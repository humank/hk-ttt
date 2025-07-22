"""
Priority enumeration for opportunity management.
Defines the priority levels for customer opportunities.
"""

from enum import Enum
from typing import Dict, Any


class Priority(Enum):
    """Enumeration for opportunity priority levels."""
    
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"
    
    def __str__(self) -> str:
        """Return string representation of priority."""
        return self.value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert priority to dictionary representation."""
        return {"priority": self.value}
    
    @classmethod
    def from_string(cls, priority_str: str) -> 'Priority':
        """Create Priority from string value."""
        for priority in cls:
            if priority.value.lower() == priority_str.lower():
                return priority
        raise ValueError(f"Invalid priority: {priority_str}")
    
    @property
    def weight(self) -> int:
        """Return numeric weight for priority comparison."""
        weights = {
            Priority.LOW: 1,
            Priority.MEDIUM: 2,
            Priority.HIGH: 3,
            Priority.CRITICAL: 4
        }
        return weights[self]
