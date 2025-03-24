from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class EmailTemplateBase(BaseModel):
    name: str
    subject: str
    body: str

class EmailTemplateCreate(EmailTemplateBase):
    pass

class EmailTemplateUpdate(EmailTemplateBase):
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None

class EmailTemplateInDBBase(EmailTemplateBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class EmailTemplate(EmailTemplateInDBBase):
    pass

class EmailTemplateInDB(EmailTemplateInDBBase):
    pass 