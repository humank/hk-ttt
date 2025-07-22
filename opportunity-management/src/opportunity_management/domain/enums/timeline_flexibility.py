"""
Timeline flexibility enumeration for opportunity timeline requirements.
"""

from enum import Enum
from typing import Dict, Any


class TimelineFlexibility(Enum):
    """Enumeration for timeline flexibility levels."""
    
    FIXED = "Fixed"
    FLEXIBLE = "Flexible"
    NEGOTIABLE = "Negotiable"
    
    def __str__(self) -> str:
        """Return string representation of timeline flexibility."""
        return self.value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert timeline flexibility to dictionary representation."""
        return {"flexibility": self.value}
    
    @classmethod
    def from_string(cls, flexibility_str: str) -> 'TimelineFlexibility':
        """Create TimelineFlexibility from string value."""
        for flexibility in cls:
            if flexibility.value.lower() == flexibility_str.lower():
                return flexibility
        raise ValueError(f"Invalid timeline flexibility: {flexibility_str}")
    
    @property
    def allows_adjustment(self) -> bool:
        """Check if timeline allows adjustments."""
        return self in [TimelineFlexibility.FLEXIBLE, TimelineFlexibility.NEGOTIABLE]
    
    @property
    def requires_approval(self) -> bool:
        """Check if timeline changes require approval."""
        return self == TimelineFlexibility.NEGOTIABLE
