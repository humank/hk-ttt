"""
Opportunity-related Pydantic schemas.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum
import uuid


class Priority(str, Enum):
    """Priority enumeration."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class OpportunityStatus(str, Enum):
    """Opportunity status enumeration."""
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class GeographicRequirements(BaseModel):
    """Geographic requirements schema."""
    region_id: uuid.UUID
    name: str
    requires_physical_presence: bool
    allows_remote_work: bool


class OpportunityCreateRequest(BaseModel):
    """Request schema for creating an opportunity."""
    title: str = Field(..., max_length=200, description="Opportunity title")
    customer_id: uuid.UUID = Field(..., description="Customer ID")
    customer_name: str = Field(..., max_length=100, description="Customer name")
    sales_manager_id: uuid.UUID = Field(..., description="Sales manager ID")
    description: str = Field(..., max_length=2000, description="Opportunity description")
    priority: Priority = Field(..., description="Opportunity priority")
    annual_recurring_revenue: float = Field(..., ge=0, description="Annual recurring revenue")
    geographic_requirements: GeographicRequirements = Field(..., description="Geographic requirements")


class OpportunityResponse(BaseModel):
    """Response schema for opportunity data."""
    id: uuid.UUID
    title: str
    customer_id: uuid.UUID
    customer_name: str
    sales_manager_id: uuid.UUID
    description: str
    priority: Priority
    annual_recurring_revenue: float
    geographic_requirements: GeographicRequirements
    status: OpportunityStatus
    created_at: datetime
    updated_at: datetime
    submitted_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    reactivation_deadline: Optional[datetime] = None

    class Config:
        from_attributes = True


class OpportunitySubmitRequest(BaseModel):
    """Request schema for submitting an opportunity."""
    user_id: uuid.UUID = Field(..., description="User ID performing the action")


class OpportunityCancelRequest(BaseModel):
    """Request schema for cancelling an opportunity."""
    user_id: uuid.UUID = Field(..., description="User ID performing the action")
    reason: str = Field(..., max_length=500, description="Cancellation reason")


class OpportunityReactivateRequest(BaseModel):
    """Request schema for reactivating an opportunity."""
    user_id: uuid.UUID = Field(..., description="User ID performing the action")


class ProblemStatementCreateRequest(BaseModel):
    """Request schema for creating a problem statement."""
    content: str = Field(..., min_length=100, max_length=5000, description="Problem statement content")


class ProblemStatementResponse(BaseModel):
    """Response schema for problem statement data."""
    id: uuid.UUID
    opportunity_id: uuid.UUID
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SkillType(str, Enum):
    """Skill type enumeration."""
    TECHNICAL = "TECHNICAL"
    SOFT = "SOFT"
    DOMAIN = "DOMAIN"


class ImportanceLevel(str, Enum):
    """Importance level enumeration."""
    MUST_HAVE = "MUST_HAVE"
    NICE_TO_HAVE = "NICE_TO_HAVE"
    PREFERRED = "PREFERRED"


class ProficiencyLevel(str, Enum):
    """Proficiency level enumeration."""
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"


class SkillRequirementCreateRequest(BaseModel):
    """Request schema for creating a skill requirement."""
    skill_id: uuid.UUID = Field(..., description="Skill ID from skills catalog")
    skill_type: SkillType = Field(..., description="Type of skill")
    importance_level: ImportanceLevel = Field(..., description="Importance level")
    minimum_proficiency_level: ProficiencyLevel = Field(..., description="Minimum proficiency level")


class SkillRequirementResponse(BaseModel):
    """Response schema for skill requirement data."""
    id: uuid.UUID
    opportunity_id: uuid.UUID
    skill_id: uuid.UUID
    skill_name: str
    skill_type: SkillType
    importance_level: ImportanceLevel
    minimum_proficiency_level: ProficiencyLevel
    created_at: datetime

    class Config:
        from_attributes = True


class TimelineRequirementCreateRequest(BaseModel):
    """Request schema for creating a timeline requirement."""
    start_date: str = Field(..., description="Start date (YYYY-MM-DD format)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD format)")
    is_flexible: bool = Field(..., description="Whether timeline is flexible")
    specific_days: Optional[List[str]] = Field(None, description="Specific days if applicable")

    @validator('start_date', 'end_date')
    def validate_date_format(cls, v):
        """Validate date format."""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')

    @validator('end_date')
    def validate_end_after_start(cls, v, values):
        """Validate end date is after start date."""
        if 'start_date' in values:
            start = datetime.strptime(values['start_date'], '%Y-%m-%d')
            end = datetime.strptime(v, '%Y-%m-%d')
            if end <= start:
                raise ValueError('End date must be after start date')
        return v


class TimelineRequirementResponse(BaseModel):
    """Response schema for timeline requirement data."""
    id: uuid.UUID
    opportunity_id: uuid.UUID
    start_date: str
    end_date: str
    is_flexible: bool
    specific_days: Optional[List[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class OpportunityStatusResponse(BaseModel):
    """Response schema for opportunity status history."""
    id: uuid.UUID
    opportunity_id: uuid.UUID
    status: OpportunityStatus
    changed_by: uuid.UUID
    reason: str
    changed_at: datetime

    class Config:
        from_attributes = True


class ChangeRecordResponse(BaseModel):
    """Response schema for change record data."""
    id: uuid.UUID
    opportunity_id: uuid.UUID
    changed_by: uuid.UUID
    field_changed: str
    reason: str
    old_value: str
    new_value: str
    changed_at: datetime

    class Config:
        from_attributes = True


class OpportunityDetailsResponse(BaseModel):
    """Response schema for detailed opportunity information."""
    opportunity: OpportunityResponse
    problem_statement: Optional[ProblemStatementResponse] = None
    skill_requirements: List[SkillRequirementResponse] = []
    timeline: Optional[TimelineRequirementResponse] = None
    status_history: List[OpportunityStatusResponse] = []
    change_history: List[ChangeRecordResponse] = []
    attachments: List[Dict[str, Any]] = []  # Will be defined in attachment schemas


class OpportunityListResponse(BaseModel):
    """Response schema for opportunity list."""
    opportunities: List[OpportunityResponse]
