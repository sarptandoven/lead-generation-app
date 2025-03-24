from fastapi import APIRouter
from app.api.api_v1.endpoints import users, leads, auth, email_templates

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(email_templates.router, prefix="/email-templates", tags=["email templates"]) 