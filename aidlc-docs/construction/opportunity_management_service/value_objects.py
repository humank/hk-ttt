"""
Value objects for the Opportunity Management Service.
"""

import uuid
from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class GeographicRequirements:
    """Geographic location requirements for an opportunity."""
    
    region_id: uuid.UUID
    name: str
    requires_physical_presence: bool
    allows_remote_work: bool

@dataclass(frozen=True)
class DateRange:
    """Date range for availability or timeline."""
    
    start_date: str  # ISO format date string
    end_date: str  # ISO format date string
    is_recurring: bool = False
    recurring_pattern: Optional[str] = None

@dataclass(frozen=True)
class Region:
    """Geographic region."""
    
    region_id: uuid.UUID
    name: str
    is_willing_to_travel: bool

@dataclass(frozen=True)
class Language:
    """Language with proficiency level."""
    
    language_id: uuid.UUID
    name: str
    proficiency_level: str  # From LanguageProficiencyLevel enum

@dataclass(frozen=True)
class Industry:
    """Industry knowledge with experience."""
    
    industry_id: uuid.UUID
    name: str
    years_of_experience: int
    specific_domains: List[str] = None

@dataclass(frozen=True)
class Skill:
    """Skill with proficiency level."""
    
    skill_id: uuid.UUID
    name: str
    proficiency_level: str  # From ProficiencyLevel enum
    years_of_experience: int
    is_custom: bool = False

@dataclass(frozen=True)
class Certification:
    """Professional certification."""
    
    name: str
    issuing_organization: str
    issue_date: str  # ISO format date string
    expiration_date: Optional[str] = None  # ISO format date string
    verification_url: Optional[str] = None
