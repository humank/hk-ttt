"""
Attachment entity for the Opportunity Management Service.
"""

import uuid
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

from .base_entity import BaseEntity

@dataclass
class Attachment(BaseEntity):
    """Attachment entity representing a file attached to provide additional context."""
    
    problem_statement_id: uuid.UUID
    file_name: str
    file_type: str
    file_size: int
    file_url: str
    uploaded_by: uuid.UUID
    uploaded_at: datetime = field(default_factory=datetime.now)
    is_removed: bool = False
    
    @staticmethod
    def create_attachment(problem_statement_id: uuid.UUID, file_name: str, file_type: str,
                         file_size: int, file_url: str, uploaded_by: uuid.UUID) -> 'Attachment':
        """Create a new attachment."""
        # Validate file size (20MB limit)
        max_size = 20 * 1024 * 1024  # 20MB in bytes
        if file_size > max_size:
            raise ValueError(f"File size exceeds the maximum allowed size of 20MB")
        
        return Attachment(
            problem_statement_id=problem_statement_id,
            file_name=file_name,
            file_type=file_type,
            file_size=file_size,
            file_url=file_url,
            uploaded_by=uploaded_by
        )
    
    def remove_attachment(self) -> None:
        """Mark the attachment as removed."""
        self.is_removed = True
        self.update()
