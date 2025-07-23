"""
Enumerations for the Opportunity Management Service.
"""

from enum import Enum, auto

class Priority(Enum):
    """Priority levels for opportunities."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class OpportunityStatus(Enum):
    """Status values for opportunities."""
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    MATCHING_IN_PROGRESS = "Matching in Progress"
    MATCHES_FOUND = "Matches Found"
    ARCHITECT_SELECTED = "Architect Selected"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class SkillType(Enum):
    """Types of skills."""
    TECHNICAL = "Technical"
    SOFT = "Soft"
    INDUSTRY = "Industry"
    LANGUAGE = "Language"

class ImportanceLevel(Enum):
    """Importance levels for skill requirements."""
    MUST_HAVE = "Must Have"
    NICE_TO_HAVE = "Nice to Have"

class ProficiencyLevel(Enum):
    """Proficiency levels for skills."""
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"

class LanguageProficiencyLevel(Enum):
    """Proficiency levels for languages."""
    BASIC = "Basic"
    CONVERSATIONAL = "Conversational"
    FLUENT = "Fluent"
    NATIVE = "Native"

class UserRole(Enum):
    """User roles in the system."""
    SOLUTION_ARCHITECT = "SolutionArchitect"
    SALES_MANAGER = "SalesManager"
    ADMIN = "Admin"

class SkillCategory(Enum):
    """Categories for skills in the Skills Catalog."""
    TECHNICAL = "Technical"
    SOFT = "Soft"
    INDUSTRY = "Industry"
    LANGUAGE = "Language"
