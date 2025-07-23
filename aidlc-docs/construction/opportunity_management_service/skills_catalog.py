"""
Skills Catalog entity for the Opportunity Management Service.
"""

import uuid
from dataclasses import dataclass, field
from typing import Optional, List

from .base_entity import BaseEntity
from .enums import SkillCategory

@dataclass
class SkillsCatalog(BaseEntity):
    """Skills Catalog entity representing a standardized skill in the system."""
    
    name: str
    category: SkillCategory
    description: str
    is_active: bool = True
    subcategory: Optional[str] = None
    related_skills: List[uuid.UUID] = field(default_factory=list)
    synonyms: List[str] = field(default_factory=list)
    
    def deactivate(self) -> None:
        """Deactivate the skill."""
        self.is_active = False
        self.update()
    
    def activate(self) -> None:
        """Activate the skill."""
        self.is_active = True
        self.update()
    
    def update_description(self, description: str) -> None:
        """Update the skill description."""
        self.description = description
        self.update()
    
    def add_related_skill(self, skill_id: uuid.UUID) -> None:
        """Add a related skill."""
        if skill_id not in self.related_skills:
            self.related_skills.append(skill_id)
            self.update()
    
    def remove_related_skill(self, skill_id: uuid.UUID) -> None:
        """Remove a related skill."""
        if skill_id in self.related_skills:
            self.related_skills.remove(skill_id)
            self.update()
    
    def add_synonym(self, synonym: str) -> None:
        """Add a synonym for the skill."""
        if synonym not in self.synonyms:
            self.synonyms.append(synonym)
            self.update()
    
    def remove_synonym(self, synonym: str) -> None:
        """Remove a synonym for the skill."""
        if synonym in self.synonyms:
            self.synonyms.remove(synonym)
            self.update()
