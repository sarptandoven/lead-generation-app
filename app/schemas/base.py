from typing import Generic, TypeVar, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')

class BaseResponse(BaseModel):
    """Base response model with common fields"""
    success: bool = Field(True, description="Whether the request was successful")
    message: Optional[str] = Field(None, description="Optional message about the response")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")

class PaginatedRequestSchema(BaseModel):
    """Base schema for paginated requests"""
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(10, ge=1, le=100, description="Number of items per page")

class PaginatedResponse(BaseResponse, Generic[T]):
    """Generic paginated response model"""
    data: T
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = Field(False, description="Always false for errors")
    error: Dict[str, Any] = Field(..., description="Error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow) 