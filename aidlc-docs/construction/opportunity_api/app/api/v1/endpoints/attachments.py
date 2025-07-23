"""
Attachment API endpoints.
"""

from fastapi import APIRouter, Depends, Request, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import uuid
import os

from app.core.database import get_db
from app.core.response import create_success_response, create_list_response
from app.core.exceptions import (
    ValidationException, NotFoundException, OperationNotAllowedException
)
from app.services.attachment_service_adapter import AttachmentServiceAdapter
from app.schemas.attachment import (
    AttachmentResponse, AttachmentListResponse, AttachmentRemoveRequest
)

router = APIRouter()


@router.post("/problem-statements/{problem_statement_id}/attachments", response_model=dict, status_code=201)
async def add_attachment(
    request: Request,
    problem_statement_id: uuid.UUID,
    file: UploadFile = File(...),
    uploaded_by: uuid.UUID = Form(...),
    db: Session = Depends(get_db)
):
    """Add an attachment to a problem statement."""
    service = AttachmentServiceAdapter(db)
    
    attachment = service.add_attachment(
        problem_statement_id=problem_statement_id,
        file=file,
        uploaded_by=uploaded_by
    )
    
    response_data = AttachmentResponse.from_orm(attachment)
    return create_success_response(request, response_data.dict(), "Attachment added successfully")


@router.get("/problem-statements/{problem_statement_id}/attachments", response_model=dict)
async def get_attachments_for_problem_statement(
    request: Request,
    problem_statement_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get all attachments for a problem statement."""
    service = AttachmentServiceAdapter(db)
    
    attachments = service.get_attachments_for_problem_statement(problem_statement_id)
    
    response_data = [AttachmentResponse.from_orm(att).dict() for att in attachments]
    
    return create_success_response(request, {"attachments": response_data}, "Attachments retrieved successfully")


@router.delete("/attachments/{attachment_id}", response_model=dict)
async def remove_attachment(
    request: Request,
    attachment_id: uuid.UUID,
    remove_data: AttachmentRemoveRequest,
    db: Session = Depends(get_db)
):
    """Remove an attachment."""
    service = AttachmentServiceAdapter(db)
    
    attachment = service.remove_attachment(attachment_id, remove_data.user_id)
    
    response_data = AttachmentResponse.from_orm(attachment)
    return create_success_response(request, response_data.dict(), "Attachment removed successfully")


@router.get("/attachments/{attachment_id}/download")
async def download_attachment(
    attachment_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Download an attachment file."""
    service = AttachmentServiceAdapter(db)
    
    attachment = service.get_attachment_by_id(attachment_id)
    
    # Check if file exists
    if not os.path.exists(attachment.file_url):
        raise NotFoundException("File not found on disk")
    
    return FileResponse(
        path=attachment.file_url,
        filename=attachment.file_name,
        media_type=attachment.file_type
    )
