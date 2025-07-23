"""
Attachment service adapter for file operations.
"""

import os
import uuid
from typing import List
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.models.attachment import Attachment
from app.models.problem_statement import ProblemStatement
from app.core.exceptions import ValidationException, NotFoundException
from app.core.config import settings


class AttachmentServiceAdapter:
    """Adapter service for attachment operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def add_attachment(
        self,
        problem_statement_id: uuid.UUID,
        file: UploadFile,
        uploaded_by: uuid.UUID
    ) -> Attachment:
        """Add an attachment to a problem statement."""
        # Validate problem statement exists
        problem_statement = self.db.query(ProblemStatement).filter(
            ProblemStatement.id == str(problem_statement_id)
        ).first()
        if not problem_statement:
            raise NotFoundException(f"Problem statement with ID {problem_statement_id} not found")
        
        # Validate file size
        if file.size and file.size > settings.MAX_FILE_SIZE:
            raise ValidationException(f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE} bytes")
        
        # Validate file type (if specific types are configured)
        if settings.ALLOWED_FILE_TYPES != ["*"]:
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in settings.ALLOWED_FILE_TYPES:
                raise ValidationException(f"File type {file_extension} is not allowed")
        
        # Create uploads directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save file to disk
        try:
            with open(file_path, "wb") as buffer:
                content = file.file.read()
                buffer.write(content)
                file_size = len(content)
        except Exception as e:
            raise ValidationException(f"Failed to save file: {str(e)}")
        
        # Create attachment record
        attachment = Attachment(
            problem_statement_id=str(problem_statement_id),
            file_name=file.filename,
            file_type=file.content_type or "application/octet-stream",
            file_size=file_size,
            file_url=file_path,
            uploaded_by=str(uploaded_by)
        )
        
        self.db.add(attachment)
        self.db.commit()
        self.db.refresh(attachment)
        
        return attachment
    
    def remove_attachment(self, attachment_id: uuid.UUID, user_id: uuid.UUID) -> Attachment:
        """Remove an attachment (mark as removed)."""
        # Validate attachment exists
        attachment = self.db.query(Attachment).filter(
            Attachment.id == str(attachment_id)
        ).first()
        if not attachment:
            raise NotFoundException(f"Attachment with ID {attachment_id} not found")
        
        if attachment.is_removed:
            raise ValidationException("Attachment is already removed")
        
        # Mark attachment as removed
        attachment.is_removed = True
        
        self.db.commit()
        self.db.refresh(attachment)
        
        return attachment
    
    def get_attachments_for_problem_statement(self, problem_statement_id: uuid.UUID) -> List[Attachment]:
        """Get all active attachments for a problem statement."""
        # Validate problem statement exists
        problem_statement = self.db.query(ProblemStatement).filter(
            ProblemStatement.id == str(problem_statement_id)
        ).first()
        if not problem_statement:
            raise NotFoundException(f"Problem statement with ID {problem_statement_id} not found")
        
        # Get active attachments
        attachments = self.db.query(Attachment).filter(
            Attachment.problem_statement_id == str(problem_statement_id),
            Attachment.is_removed == False
        ).all()
        
        return attachments
    
    def get_attachment_by_id(self, attachment_id: uuid.UUID) -> Attachment:
        """Get attachment by ID."""
        attachment = self.db.query(Attachment).filter(
            Attachment.id == str(attachment_id)
        ).first()
        if not attachment:
            raise NotFoundException(f"Attachment with ID {attachment_id} not found")
        
        if attachment.is_removed:
            raise NotFoundException("Attachment has been removed")
        
        return attachment
