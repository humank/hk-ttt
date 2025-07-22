"""
Base entity class providing common functionality for all domain entities.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any
import uuid


@dataclass
class BaseEntity:
    """Base class for all domain entities with common functionality."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: int = field(default=1)
    
    def __post_init__(self):
        """Post-initialization validation and setup."""
        if not self.id:
            self.id = str(uuid.uuid4())
        
        if not self.created_at:
            self.created_at = datetime.utcnow()
        
        if not self.updated_at:
            self.updated_at = datetime.utcnow()
    
    def update_timestamp(self) -> None:
        """Update the entity's timestamp and increment version."""
        self.updated_at = datetime.utcnow()
        self.version += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary representation."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version
        }
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update entity from dictionary data."""
        if "updated_at" in data:
            self.updated_at = datetime.fromisoformat(data["updated_at"])
        if "version" in data:
            self.version = data["version"]
    
    @property
    def is_new(self) -> bool:
        """Check if this is a new entity (version 1)."""
        return self.version == 1
    
    @property
    def age_in_days(self) -> int:
        """Get the age of the entity in days."""
        return (datetime.utcnow() - self.created_at).days
    
    def __eq__(self, other) -> bool:
        """Check equality based on entity ID."""
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash based on entity ID."""
        return hash(self.id)
