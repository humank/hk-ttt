"""
Skill requirement value object for opportunity skill specifications.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from ..enums.skill_importance import SkillImportance


@dataclass(frozen=True)
class SkillRequirement:
    """Value object representing a skill requirement for an opportunity."""
    
    skill_name: str
    skill_category: str  # Technical, Soft, Industry
    importance: SkillImportance
    proficiency_level: Optional[str] = None  # Beginner, Intermediate, Advanced, Expert
    description: Optional[str] = None
    
    def __post_init__(self):
        """Validate skill requirement after initialization."""
        if not self.skill_name or not self.skill_name.strip():
            raise ValueError("Skill name cannot be empty")
        
        if not self.skill_category or not self.skill_category.strip():
            raise ValueError("Skill category cannot be empty")
        
        valid_categories = ["Technical", "Soft", "Industry"]
        if self.skill_category not in valid_categories:
            raise ValueError(f"Skill category must be one of: {valid_categories}")
        
        if self.proficiency_level:
            valid_levels = ["Beginner", "Intermediate", "Advanced", "Expert"]
            if self.proficiency_level not in valid_levels:
                raise ValueError(f"Proficiency level must be one of: {valid_levels}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert skill requirement to dictionary representation."""
        return {
            "skill_name": self.skill_name,
            "skill_category": self.skill_category,
            "importance": self.importance.value,
            "proficiency_level": self.proficiency_level,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillRequirement':
        """Create SkillRequirement from dictionary."""
        return cls(
            skill_name=data["skill_name"],
            skill_category=data["skill_category"],
            importance=SkillImportance.from_string(data["importance"]),
            proficiency_level=data.get("proficiency_level"),
            description=data.get("description")
        )
    
    @property
    def is_mandatory(self) -> bool:
        """Check if this skill requirement is mandatory."""
        return self.importance.is_mandatory
    
    def matches_skill(self, skill_name: str, proficiency: Optional[str] = None) -> bool:
        """Check if this requirement matches a given skill."""
        if self.skill_name.lower() != skill_name.lower():
            return False
        
        if self.proficiency_level and proficiency:
            proficiency_order = ["Beginner", "Intermediate", "Advanced", "Expert"]
            required_level = proficiency_order.index(self.proficiency_level)
            actual_level = proficiency_order.index(proficiency)
            return actual_level >= required_level
        
        return True
