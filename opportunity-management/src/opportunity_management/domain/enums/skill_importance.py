"""
Skill importance enumeration for skill requirements.
"""

from enum import Enum
from typing import Dict, Any


class SkillImportance(Enum):
    """Enumeration for skill importance levels."""
    
    MUST_HAVE = "Must Have"
    NICE_TO_HAVE = "Nice to Have"
    
    def __str__(self) -> str:
        """Return string representation of skill importance."""
        return self.value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert skill importance to dictionary representation."""
        return {"importance": self.value}
    
    @classmethod
    def from_string(cls, importance_str: str) -> 'SkillImportance':
        """Create SkillImportance from string value."""
        for importance in cls:
            if importance.value.lower() == importance_str.lower():
                return importance
        raise ValueError(f"Invalid skill importance: {importance_str}")
    
    @property
    def weight(self) -> int:
        """Return numeric weight for importance comparison."""
        weights = {
            SkillImportance.NICE_TO_HAVE: 1,
            SkillImportance.MUST_HAVE: 2
        }
        return weights[self]
    
    @property
    def is_mandatory(self) -> bool:
        """Check if this importance level is mandatory."""
        return self == SkillImportance.MUST_HAVE
