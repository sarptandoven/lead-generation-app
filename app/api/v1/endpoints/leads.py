from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel, Field, conlist
from app.services.lead_generation import LeadGenerationService

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

class LeadScore(BaseModel):
    relevance: float = Field(..., ge=0, le=100)
    engagement: float = Field(..., ge=0, le=100)
    potential: float = Field(..., ge=0, le=100)
    total: float = Field(..., ge=0, le=100)

class LeadResponse(BaseModel):
    name: str = Field(..., description="Full name of the lead")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Location")
    email: Optional[str] = Field(None, description="Email address if available")
    phone: Optional[str] = Field(None, description="Phone number if available")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL if available")
    score: LeadScore = Field(..., description="Lead scoring metrics")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional lead information")

    class Config:
        schema_extra = {
            "example": {
                "name": "John Smith",
                "title": "Senior Property Manager",
                "company": "ABC Properties",
                "location": "New York, NY",
                "email": "john.smith@abcproperties.com",
                "phone": "+1-555-0123",
                "linkedin_url": "https://linkedin.com/in/johnsmith",
                "score": {
                    "relevance": 85,
                    "engagement": 75,
                    "potential": 90,
                    "total": 83
                },
                "metadata": {
                    "portfolio_size": 150,
                    "property_types": ["residential", "commercial"],
                    "experience_years": 8
                }
            }
        }

class LeadAnalysis(BaseModel):
    analysis: str = Field(..., description="Detailed analysis of the leads")
    timestamp: str = Field(..., description="Timestamp of the analysis")

@router.post("/generate", response_model=List[LeadResponse], tags=["leads"])
async def generate_leads(
    criteria: SearchCriteria,
    include_analysis: bool = Query(False, description="Whether to include lead analysis in response")
) -> List[LeadResponse]:
    """
    Generate leads based on search criteria.
    
    - Searches for property management professionals matching the specified criteria
    - Scores and ranks leads based on relevance, engagement, and potential
    - Optionally includes detailed analysis of the lead set
    """
    try:
        search_params = criteria.dict()
        max_leads = search_params.pop('max_leads')
        
        leads = await lead_service.generate_leads(
            search_criteria=search_params,
            max_leads=max_leads
        )
        
        if include_analysis and leads:
            analysis = await lead_service.analyze_leads(leads)
            for lead in leads:
                lead['metadata']['analysis'] = analysis
        
        return leads
    except Exception as e:
        logger.error(f"Failed to generate leads: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate leads: {str(e)}"
        )

@router.post("/analyze", response_model=LeadAnalysis, tags=["leads"])
async def analyze_leads(leads: List[LeadResponse]) -> LeadAnalysis:
    """
    Analyze a batch of leads to provide insights.
    
    - Evaluates the overall quality of the lead set
    - Identifies common patterns and trends
    - Suggests prioritization strategies
    - Recommends engagement approaches
    """
    try:
        return await lead_service.analyze_leads(leads)
    except Exception as e:
        logger.error(f"Failed to analyze leads: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze leads: {str(e)}"
        )

@router.get("/export", tags=["leads"])
async def export_leads(
    format: str = Query('csv', regex='^csv$', description="Export format (currently only CSV is supported)"),
    max_leads: int = Query(100, ge=1, le=1000, description="Maximum number of leads to export")
) -> Response:
    """
    Export leads to CSV format.
    
    - Retrieves leads using default search criteria
    - Formats the data for export
    - Returns a downloadable file
    """
    try:
        # Get leads with default criteria
        leads = await lead_service.generate_leads({}, max_leads=max_leads)
        
        # Export leads
        export_data = await lead_service.export_leads(leads, format=format)
        
        # Return the exported data as a downloadable file
        headers = {
            'Content-Disposition': f'attachment; filename="leads.{format}"',
            'Content-Type': 'text/csv'
        }
        
        return Response(
            content=export_data,
            media_type='text/csv',
            headers=headers
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to export leads: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export leads: {str(e)}"
        ) 