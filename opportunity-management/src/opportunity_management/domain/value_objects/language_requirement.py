"""
Language requirement value object for opportunity language specifications.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from ..enums.skill_importance import SkillImportance


@dataclass(frozen=True)
class LanguageRequirement:
    """Value object representing language requirements for an opportunity."""
    
    language: str
    proficiency_level: str  # Basic, Conversational, Business, Native
    importance: SkillImportance
    context: Optional[str] = None  # e.g., "Client communication", "Technical documentation"
    
    def __post_init__(self):
        """Validate language requirement after initialization."""
        if not self.language or not self.language.strip():
            raise ValueError("Language cannot be empty")
        
        valid_levels = ["Basic", "Conversational", "Business", "Native"]
        if self.proficiency_level not in valid_levels:
            raise ValueError(f"Proficiency level must be one of: {valid_levels}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert language requirement to dictionary representation."""
        return {
            "language": self.language,
            "proficiency_level": self.proficiency_level,
            "importance": self.importance.value,
            "context": self.context
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LanguageRequirement':
        """Create LanguageRequirement from dictionary."""
        return cls(
            language=data["language"],
            proficiency_level=data["proficiency_level"],
            importance=SkillImportance.from_string(data["importance"]),
            context=data.get("context")
        )
    
    def meets_requirement(self, language: str, proficiency: str) -> bool:
        """Check if given language and proficiency meets this requirement."""
        if self.language.lower() != language.lower():
            return False
        
        proficiency_order = ["Basic", "Conversational", "Business", "Native"]
        required_level = proficiency_order.index(self.proficiency_level)
        actual_level = proficiency_order.index(proficiency)
        
        return actual_level >= required_level
    
    @property
    def is_mandatory(self) -> bool:
        """Check if this language requirement is mandatory."""
        return self.importance.is_mandatory


@dataclass(frozen=True)
class LanguageRequirements:
    """Collection of language requirements for an opportunity."""
    
    requirements: List[LanguageRequirement]
    
    def __post_init__(self):
        """Validate language requirements collection."""
        if not self.requirements:
            raise ValueError("At least one language requirement must be specified")
        
        # Check for duplicate languages
        languages = [req.language.lower() for req in self.requirements]
        if len(languages) != len(set(languages)):
            raise ValueError("Duplicate language requirements are not allowed")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert language requirements to dictionary representation."""
        return {
            "requirements": [req.to_dict() for req in self.requirements]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LanguageRequirements':
        """Create LanguageRequirements from dictionary."""
        requirements = [LanguageRequirement.from_dict(req_data) 
                       for req_data in data["requirements"]]
        return cls(requirements=requirements)
    
    def get_mandatory_languages(self) -> List[LanguageRequirement]:
        """Get all mandatory language requirements."""
        return [req for req in self.requirements if req.is_mandatory]
    
    def get_optional_languages(self) -> List[LanguageRequirement]:
        """Get all optional language requirements."""
        return [req for req in self.requirements if not req.is_mandatory]
