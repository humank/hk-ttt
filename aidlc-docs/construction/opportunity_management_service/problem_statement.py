"""
ProblemStatement entity for the Opportunity Management Service.
"""

import uuid
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

from .base_entity import BaseEntity
from .common import ValidationException

@dataclass
class ProblemStatement(BaseEntity):
    """ProblemStatement entity representing a detailed description of the customer's problem."""
    
    opportunity_id: uuid.UUID
    content: str
    minimum_character_count: int = 140  # As per clarification
    
    def __post_init__(self):
        """Validate the problem statement after initialization."""
        self.validate_content()
    
    @staticmethod
    def create_problem_statement(opportunity_id: uuid.UUID, content: str) -> 'ProblemStatement':
        """Create a new problem statement."""
        problem_statement = ProblemStatement(
            opportunity_id=opportunity_id,
            content=content
        )
        return problem_statement
    
    def update_content(self, new_content: str) -> None:
        """Update the content of the problem statement."""
        self.content = new_content
        self.validate_content()
        self.update()
    
    def validate_content(self) -> bool:
        """Validate that the content meets the minimum character requirement."""
        if len(self.content) < self.minimum_character_count:
            raise ValidationException(
                f"Problem statement must be at least {self.minimum_character_count} characters long"
            )
        return True
    
    def preview_content(self) -> str:
        """Return a preview of the content."""
        # In a real implementation, this might render the rich text content
        # For simplicity, we'll just return the first 100 characters
        preview_length = min(100, len(self.content))
        preview = self.content[:preview_length]
        if len(self.content) > preview_length:
            preview += "..."
        return preview
