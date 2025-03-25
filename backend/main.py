from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Lead Generation API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuthResponse(BaseModel):
    is_admin: bool
    message: str

@app.get("/")
async def root():
    return {"message": "API is working!"}

@app.post("/api/auth/check")
async def check_auth():
    # For demo purposes, always return non-admin
    return AuthResponse(
        is_admin=False,
        message="Non-administrators cannot pull LinkedIn user information."
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
