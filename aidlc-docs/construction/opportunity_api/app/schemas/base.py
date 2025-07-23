"""
Base schemas for common response structures.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class ResponseMeta(BaseModel):
    """Response metadata."""
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: str


class PaginationInfo(BaseModel):
    """Pagination information."""
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class StandardResponse(BaseModel):
    """Standard API response wrapper."""
    data: Dict[str, Any]
    meta: ResponseMeta
    pagination: Optional[PaginationInfo] = None


class ErrorDetail(BaseModel):
    """Error detail information."""
    field: str
    message: str


class ErrorInfo(BaseModel):
    """Error information."""
    code: str = Field(
        description="Error code",
        examples=["VALIDATION_ERROR", "RESOURCE_NOT_FOUND", "OPERATION_NOT_ALLOWED", "INTERNAL_ERROR"]
    )
    message: str = Field(description="Error message")
    details: List[ErrorDetail] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    """Error response structure."""
    error: ErrorInfo
    meta: ResponseMeta


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = "1.0.0"
