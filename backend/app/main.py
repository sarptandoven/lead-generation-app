from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from .core.config import settings
from .core.database import SessionLocal, engine
from .models import models
from .services import linkedin_scraper, airbnb_scraper, web_scraper
from .services.ai_service import AIService
from .utils.rate_limiter import RateLimiter

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(
    filename=settings.LOG_FILE,
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Lead Generation API",
    description="AI-powered lead generation system for property managers",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Rate limiter
rate_limiter = RateLimiter(
    max_requests_per_minute=settings.MAX_REQUESTS_PER_MINUTE,
    max_requests_per_hour=settings.MAX_REQUESTS_PER_HOUR
)

# AI Service
ai_service = AIService(api_key=settings.OPENAI_API_KEY)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Lead(BaseModel):
    name: str
    title: str
    company: str
    location: str
    email: Optional[str] = None
    phone: Optional[str] = None
    source: str
    score: Optional[float] = None

class ScrapingRequest(BaseModel):
    source: str
    parameters: dict
    background: bool = True

# Authentication
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm="HS256")
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.APP_SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/scrape", response_model=List[Lead])
async def start_scraping(
    request: ScrapingRequest,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not rate_limiter.check_rate_limit(current_user.username):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    async def process_leads(leads: List[Lead]):
        for lead in leads:
            # Enrich lead data with AI
            enriched_data = await ai_service.enrich_lead(lead)
            # Store in database
            db_lead = models.Lead(**enriched_data.dict())
            db.add(db_lead)
        db.commit()

    if request.source == "linkedin":
        leads = await linkedin_scraper.scrape_leads(request.parameters)
    elif request.source == "airbnb":
        leads = await airbnb_scraper.scrape_leads(request.parameters)
    elif request.source == "web":
        leads = await web_scraper.scrape_leads(request.parameters)
    else:
        raise HTTPException(status_code=400, detail="Invalid source")

    if request.background:
        background_tasks.add_task(process_leads, leads)
        return {"message": "Scraping started in background"}
    else:
        await process_leads(leads)
        return leads

@app.get("/leads", response_model=List[Lead])
async def get_leads(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    leads = db.query(models.Lead).offset(skip).limit(limit).all()
    return leads

@app.get("/leads/{lead_id}", response_model=Lead)
async def get_lead(
    lead_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@app.get("/stats")
async def get_stats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_leads = db.query(models.Lead).count()
    leads_by_source = db.query(
        models.Lead.source,
        func.count(models.Lead.id)
    ).group_by(models.Lead.source).all()
    
    return {
        "total_leads": total_leads,
        "leads_by_source": dict(leads_by_source)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 