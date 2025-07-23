"""
Attachment-related Pydantic schemas.
"""

from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi import UploadFile
import uuid


class AttachmentCreateRequest(BaseModel):
    """Request schema for creating an attachment."""
    uploaded_by: uuid.UUID = Field(..., description="User ID who uploaded the file")
    
    # Note: file will be handled separately as UploadFile in the endpoint


class AttachmentResponse(BaseModel):
    """Response schema for attachment data."""
    id: uuid.UUID
    problem_statement_id: uuid.UUID
    file_name: str
    file_type: str
    file_size: int
    file_url: str
    uploaded_by: uuid.UUID
    uploaded_at: datetime
    is_removed: bool = False

    class Config:
        from_attributes = True


class AttachmentListResponse(BaseModel):
    """Response schema for attachment list."""
    attachments: List[AttachmentResponse]


class AttachmentRemoveRequest(BaseModel):
    """Request schema for removing an attachment."""
    user_id: uuid.UUID = Field(..., description="User ID performing the action")
