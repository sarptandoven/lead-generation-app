from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from .base import BaseResponse

class LeadBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    linkedin_url: Optional[str] = None
    status: Optional[str] = "new"
    notes: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(LeadBase):
    pass

class LeadInDBBase(LeadBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    last_contact_at: Optional[datetime]

    class Config:
        orm_mode = True

class Lead(LeadInDBBase):
    pass

class LeadInDB(LeadInDBBase):
    pass

class LeadScore(BaseModel):
    """Model for lead scoring results"""
    total_score: float = Field(..., ge=0.0, le=1.0, description="Overall lead score")
    property_fit: float = Field(..., ge=0.0, le=1.0, description="Score for property size fit")
    decision_maker: float = Field(..., ge=0.0, le=1.0, description="Score for decision-making authority")
    location_value: float = Field(..., ge=0.0, le=1.0, description="Score for location value")
    response_likelihood: float = Field(..., ge=0.0, le=1.0, description="Score for likelihood of response")
    notes: Optional[str] = Field(None, description="Additional notes about the scoring")

class LeadRequest(BaseModel):
    """Model for lead generation request"""
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

class Lead(BaseModel):
    """Model for lead information"""
    name: str = Field(..., description="Full name of the lead")
    company: str = Field(..., description="Company name")
    title: Optional[str] = Field(None, description="Job title")
    location: Optional[str] = Field(None, description="Location")
    website: Optional[str] = Field(None, description="Company website URL")
    phone: Optional[str] = Field(None, description="Contact phone number")
    email: Optional[EmailStr] = Field(None, description="Contact email")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    properties: Optional[int] = Field(None, description="Number of properties managed")
    source: str = Field(..., description="Source of the lead data")
    score: Optional[LeadScore] = Field(None, description="Lead scoring results")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Smith",
                "company": "ABC Property Management",
                "title": "Senior Property Manager",
                "location": "New York, NY",
                "website": "https://www.abcproperties.com",
                "phone": "+1-555-0123",
                "email": "john.smith@abcproperties.com",
                "linkedin_url": "https://linkedin.com/in/johnsmith",
                "properties": 15,
                "source": "linkedin",
                "score": {
                    "total_score": 0.85,
                    "property_fit": 0.9,
                    "decision_maker": 0.8,
                    "location_value": 0.85,
                    "response_likelihood": 0.85,
                    "notes": "Strong candidate with relevant experience"
                }
            }
        }

class LeadAnalysisRequest(BaseModel):
    """Model for lead analysis request"""
    leads: List[Lead] = Field(..., description="List of leads to analyze")

class LeadResponse(BaseResponse):
    """Model for lead response"""
    data: List[Lead]

class LeadAnalysisResponse(BaseResponse):
    """Model for lead analysis response"""
    data: List[Lead]
    analysis_summary: Optional[str] = Field(None, description="Summary of the analysis") 