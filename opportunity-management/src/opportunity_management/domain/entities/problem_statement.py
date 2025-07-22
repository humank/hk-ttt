"""
Problem statement entity for opportunity management.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from .base_entity import BaseEntity
from ..value_objects.document_attachment import DocumentAttachment


@dataclass
class ProblemStatement(BaseEntity):
    """Entity representing a problem statement for an opportunity."""
    
    title: str = ""
    description: str = ""
    business_impact: Optional[str] = None
    technical_requirements: Optional[str] = None
    success_criteria: Optional[str] = None
    constraints: Optional[str] = None
    attachments: List[DocumentAttachment] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate problem statement after initialization."""
        super().__post_init__()
        
        if not self.title or not self.title.strip():
            raise ValueError("Problem statement title cannot be empty")
        
        if not self.description or not self.description.strip():
            raise ValueError("Problem statement description cannot be empty")
        
        # Minimum character requirement for detailed description
        if len(self.description.strip()) < 50:
            raise ValueError("Problem statement description must be at least 50 characters")
    
    def update_description(self, description: str) -> None:
        """Update the problem statement description."""
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")
        
        if len(description.strip()) < 50:
            raise ValueError("Description must be at least 50 characters")
        
        self.description = description
        self.update_timestamp()
    
    def update_business_impact(self, business_impact: str) -> None:
        """Update the business impact section."""
        self.business_impact = business_impact
        self.update_timestamp()
    
    def update_technical_requirements(self, technical_requirements: str) -> None:
        """Update the technical requirements section."""
        self.technical_requirements = technical_requirements
        self.update_timestamp()
    
    def update_success_criteria(self, success_criteria: str) -> None:
        """Update the success criteria section."""
        self.success_criteria = success_criteria
        self.update_timestamp()
    
    def update_constraints(self, constraints: str) -> None:
        """Update the constraints section."""
        self.constraints = constraints
        self.update_timestamp()
    
    def add_attachment(self, attachment: DocumentAttachment) -> None:
        """Add a document attachment to the problem statement."""
        if attachment in self.attachments:
            raise ValueError("Attachment already exists")
        
        self.attachments.append(attachment)
        self.update_timestamp()
    
    def remove_attachment(self, file_id: str) -> bool:
        """Remove a document attachment by file ID."""
        for i, attachment in enumerate(self.attachments):
            if attachment.file_id == file_id:
                del self.attachments[i]
                self.update_timestamp()
                return True
        return False
    
    def get_attachment(self, file_id: str) -> Optional[DocumentAttachment]:
        """Get a document attachment by file ID."""
        for attachment in self.attachments:
            if attachment.file_id == file_id:
                return attachment
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert problem statement to dictionary representation."""
        base_dict = super().to_dict()
        base_dict.update({
            "title": self.title,
            "description": self.description,
            "business_impact": self.business_impact,
            "technical_requirements": self.technical_requirements,
            "success_criteria": self.success_criteria,
            "constraints": self.constraints,
            "attachments": [attachment.to_dict() for attachment in self.attachments]
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProblemStatement':
        """Create ProblemStatement from dictionary."""
        attachments = [DocumentAttachment.from_dict(att_data) 
                      for att_data in data.get("attachments", [])]
        
        problem_statement = cls(
            title=data["title"],
            description=data["description"],
            business_impact=data.get("business_impact"),
            technical_requirements=data.get("technical_requirements"),
            success_criteria=data.get("success_criteria"),
            constraints=data.get("constraints"),
            attachments=attachments
        )
        problem_statement.update_from_dict(data)
        return problem_statement
    
    @property
    def is_complete(self) -> bool:
        """Check if the problem statement has all recommended sections."""
        return all([
            self.title,
            self.description,
            self.business_impact,
            self.technical_requirements,
            self.success_criteria
        ])
    
    @property
    def attachment_count(self) -> int:
        """Get the number of attachments."""
        return len(self.attachments)
    
    @property
    def total_attachment_size_mb(self) -> float:
        """Get total size of all attachments in MB."""
        return sum(attachment.file_size_mb for attachment in self.attachments)
    
    def __str__(self) -> str:
        """String representation of problem statement."""
        return f"ProblemStatement(id={self.id}, title={self.title})"
