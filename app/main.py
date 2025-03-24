from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
from app.api.v1.endpoints import leads

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Lead Generation API",
    description="API for generating and analyzing property manager leads",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API routes
app.include_router(
    leads.router,
    prefix="/api/v1/leads",
    tags=["leads"]
)

@app.get("/")
async def root():
    """Root endpoint that redirects to the static index.html"""
    return {"message": "Welcome to the Lead Generation API"}

@app.on_event("startup")
async def startup_event():
    """Initialize services and connections on startup."""
    logger.info("Starting Lead Generation API")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Shutting down Lead Generation API") 