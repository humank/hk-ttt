"""
Document attachment value object for opportunity document management.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
import uuid


@dataclass(frozen=True)
class DocumentAttachment:
    """Value object representing a document attachment for an opportunity."""
    
    file_id: str
    file_name: str
    file_size_bytes: int
    file_type: str
    upload_timestamp: datetime
    uploaded_by: str
    description: Optional[str] = None
    
    def __post_init__(self):
        """Validate document attachment after initialization."""
        if not self.file_name or not self.file_name.strip():
            raise ValueError("File name cannot be empty")
        
        if self.file_size_bytes <= 0:
            raise ValueError("File size must be positive")
        
        # 20MB limit as specified in requirements
        max_size_bytes = 20 * 1024 * 1024  # 20MB
        if self.file_size_bytes > max_size_bytes:
            raise ValueError(f"File size exceeds maximum limit of {max_size_bytes} bytes")
        
        if not self.file_type or not self.file_type.strip():
            raise ValueError("File type cannot be empty")
        
        if not self.uploaded_by or not self.uploaded_by.strip():
            raise ValueError("Uploaded by cannot be empty")
    
    @classmethod
    def create_new(cls, file_name: str, file_size_bytes: int, file_type: str, 
                   uploaded_by: str, description: Optional[str] = None) -> 'DocumentAttachment':
        """Create a new document attachment with generated ID and timestamp."""
        return cls(
            file_id=str(uuid.uuid4()),
            file_name=file_name,
            file_size_bytes=file_size_bytes,
            file_type=file_type,
            upload_timestamp=datetime.utcnow(),
            uploaded_by=uploaded_by,
            description=description
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document attachment to dictionary representation."""
        return {
            "file_id": self.file_id,
            "file_name": self.file_name,
            "file_size_bytes": self.file_size_bytes,
            "file_type": self.file_type,
            "upload_timestamp": self.upload_timestamp.isoformat(),
            "uploaded_by": self.uploaded_by,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentAttachment':
        """Create DocumentAttachment from dictionary."""
        return cls(
            file_id=data["file_id"],
            file_name=data["file_name"],
            file_size_bytes=data["file_size_bytes"],
            file_type=data["file_type"],
            upload_timestamp=datetime.fromisoformat(data["upload_timestamp"]),
            uploaded_by=data["uploaded_by"],
            description=data.get("description")
        )
    
    @property
    def file_size_mb(self) -> float:
        """Get file size in megabytes."""
        return self.file_size_bytes / (1024 * 1024)
    
    @property
    def is_image(self) -> bool:
        """Check if the attachment is an image file."""
        image_types = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp']
        return self.file_type.lower() in image_types
    
    @property
    def is_document(self) -> bool:
        """Check if the attachment is a document file."""
        document_types = ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt']
        return self.file_type.lower() in document_types
