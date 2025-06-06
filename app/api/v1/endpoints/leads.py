from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import Response
from pydantic import BaseModel, Field, conlist
from app.schemas.lead import (
    LeadRequest, 
    LeadResponse, 
    LeadAnalysisRequest, 
    LeadAnalysisResponse,
    Lead
)
from app.services.lead_generation import LeadGenerationService
from app.services.lead_scoring import LeadScore
from app.core.config import settings

router = APIRouter()
lead_service = LeadGenerationService()

class SearchCriteria(BaseModel):
    keywords: conlist(str, min_items=1) = Field(..., description="List of keywords to search for")
    location: Optional[str] = Field(None, description="Location to filter leads by")
    industry: Optional[str] = Field(None, description="Industry to filter leads by")
    company_size: Optional[str] = Field(None, description="Company size to filter by")
    max_leads: Optional[int] = Field(10, ge=1, le=100, description="Maximum number of leads to return")

    class Config:
        schema_extra = {
            "example": {
                "keywords": ["property manager", "real estate"],
                "location": "New York",
                "industry": "Real Estate",
                "company_size": "10-50",
                "max_leads": 20
            }
        }

class LeadRequest(BaseModel):
    location: str = Field(..., description="Target location for lead search")
    properties_range: str = Field(
        ..., 
        description="Range of properties managed",
        regex="^(1-7|8-15|15-24|25\+)$"
    )
    max_leads: Optional[int] = Field(
        25, 
        description="Maximum number of leads to return",
        gt=0,
        le=100
    )
    min_score: Optional[float] = Field(
        0.7,
        description="Minimum score threshold (0.0 to 1.0)",
        ge=0.0,
        le=1.0
    )

class LeadResponse(BaseModel):
    name: str
    company: str
    title: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    properties: Optional[int] = None
    source: str
    score: LeadScore

class LeadAnalysisRequest(BaseModel):
    leads: List[dict] = Field(..., description="List of leads to analyze")

class LeadAnalysis(BaseModel):
    analysis: str = Field(..., description="Detailed analysis of the leads")
    timestamp: str = Field(..., description="Timestamp of the analysis")

@router.post("/generate", response_model=LeadResponse)
async def generate_leads(request: LeadRequest):
    """
    Generate and score property manager leads based on location and criteria.
    
    This endpoint will:
    1. Search for property managers in the specified location
    2. Filter by property range
    3. Score leads using AI
    4. Return qualified leads sorted by score
    """
    try:
        leads = await lead_service.generate_leads(
            location=request.location,
            properties_range=request.properties_range,
            max_leads=request.max_leads,
            min_score=request.min_score
        )
        
        return LeadResponse(
            data=leads,
            message=f"Successfully generated {len(leads)} leads"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating leads: {str(e)}"
        )

@router.post("/analyze", response_model=LeadAnalysisResponse)
async def analyze_leads(request: LeadAnalysisRequest):
    """
    Analyze and score a list of existing leads.
    
    This endpoint will:
    1. Score each lead using AI
    2. Provide detailed analysis
    3. Return scored leads with insights
    """
    try:
        analyzed_leads = await lead_service.analyze_leads(request.leads)
        
        return LeadAnalysisResponse(
            data=analyzed_leads,
            message=f"Successfully analyzed {len(analyzed_leads)} leads"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing leads: {str(e)}"
        )

@router.get("/export")
async def export_leads(
    leads: List[Lead] = Query(...),
    format: str = Query("csv", regex="^(csv|xlsx)$")
):
    """
    Export leads to CSV or Excel format.
    
    This endpoint will:
    1. Take a list of leads
    2. Convert them to the specified format
    3. Return a downloadable file
    """
    try:
        file_data = await lead_service.export_leads(leads, format)
        
        headers = {
            "Content-Disposition": f"attachment; filename=leads.{format}",
            "Content-Type": "application/octet-stream"
        }
        
        return Response(
            content=file_data,
            headers=headers
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error exporting leads: {str(e)}"
        ) 