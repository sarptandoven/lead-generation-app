from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

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