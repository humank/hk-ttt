"""
Base entity class for the Opportunity Management Service.
"""

import uuid
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class BaseEntity:
    """Base class for all entities in the domain model."""
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def update(self) -> None:
        """Update the entity's last modified timestamp."""
        self.updated_at = datetime.now()
    
    def __eq__(self, other):
        """Entities are equal if their IDs are equal."""
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id
    
    def __hash__(self):
        """Hash based on the entity's ID."""
        return hash(self.id)
