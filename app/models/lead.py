from sqlalchemy import Boolean, Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Lead(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True)
    company = Column(String, index=True)
    position = Column(String)
    linkedin_url = Column(String)
    status = Column(String, default="new")  # new, contacted, responded, qualified, converted
    notes = Column(String)
    data = Column(JSON)  # Additional scraped data
    
    # Relationships
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="leads")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_contact_at = Column(DateTime(timezone=True)) 