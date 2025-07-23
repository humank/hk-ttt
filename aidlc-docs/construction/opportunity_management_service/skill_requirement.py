"""
SkillRequirement entity for the Opportunity Management Service.
"""

import uuid
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

from .base_entity import BaseEntity
from .enums import SkillType, ImportanceLevel, ProficiencyLevel

@dataclass
class SkillRequirement(BaseEntity):
    """SkillRequirement entity representing a specific skill required for an opportunity."""
    
    opportunity_id: uuid.UUID
    skill_id: uuid.UUID
    skill_name: str
    skill_type: SkillType
    importance_level: ImportanceLevel
    minimum_proficiency_level: ProficiencyLevel
    
    @staticmethod
    def create_skill_requirement(opportunity_id: uuid.UUID, skill_id: uuid.UUID, skill_name: str,
                               skill_type: SkillType, importance_level: ImportanceLevel,
                               minimum_proficiency_level: ProficiencyLevel) -> 'SkillRequirement':
        """Create a new skill requirement."""
        return SkillRequirement(
            opportunity_id=opportunity_id,
            skill_id=skill_id,
            skill_name=skill_name,
            skill_type=skill_type,
            importance_level=importance_level,
            minimum_proficiency_level=minimum_proficiency_level
        )
    
    def update_importance_level(self, new_level: ImportanceLevel) -> None:
        """Update the importance level of the skill requirement."""
        self.importance_level = new_level
        self.update()
    
    def update_proficiency_level(self, new_level: ProficiencyLevel) -> None:
        """Update the minimum proficiency level of the skill requirement."""
        self.minimum_proficiency_level = new_level
        self.update()
