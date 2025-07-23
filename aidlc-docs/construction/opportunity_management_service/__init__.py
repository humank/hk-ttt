"""
Opportunity Management Service package.
"""

# Import main components for easier access
from .enums import (
    Priority, OpportunityStatus, SkillType, ImportanceLevel, 
    ProficiencyLevel, UserRole, SkillCategory, LanguageProficiencyLevel
)
from .value_objects import (
    GeographicRequirements, DateRange, Region, Language, 
    Industry, Skill, Certification
)
from .base_entity import BaseEntity
from .user import User
