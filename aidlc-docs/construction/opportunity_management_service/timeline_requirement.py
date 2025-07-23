"""
TimelineRequirement entity for the Opportunity Management Service.
"""

import uuid
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime, date
from dateutil.parser import parse

from .base_entity import BaseEntity
from .common import ValidationException

@dataclass
class TimelineRequirement(BaseEntity):
    """TimelineRequirement entity representing the timeline specifications for an opportunity."""
    
    opportunity_id: uuid.UUID
    expected_start_date: str  # ISO format date string
    expected_end_date: str  # ISO format date string
    is_flexible: bool
    specific_required_days: List[str] = field(default_factory=list)  # List of ISO format date strings
    
    def __post_init__(self):
        """Validate the timeline requirement after initialization."""
        self.validate_timeline()
    
    @staticmethod
    def create_timeline_requirement(opportunity_id: uuid.UUID, start_date: str, end_date: str,
                                  is_flexible: bool, specific_days: Optional[List[str]] = None) -> 'TimelineRequirement':
        """Create a new timeline requirement."""
        timeline = TimelineRequirement(
            opportunity_id=opportunity_id,
            expected_start_date=start_date,
            expected_end_date=end_date,
            is_flexible=is_flexible,
            specific_required_days=specific_days or []
        )
        return timeline
    
    def update_dates(self, start_date: str, end_date: str) -> None:
        """Update the start and end dates of the timeline requirement."""
        self.expected_start_date = start_date
        self.expected_end_date = end_date
        self.validate_timeline()
        self.update()
    
    def update_specific_days(self, specific_days: List[str]) -> None:
        """Update the specific required days of the timeline requirement."""
        self.specific_required_days = specific_days
        self.validate_timeline()
        self.update()
    
    def update_flexibility(self, is_flexible: bool) -> None:
        """Update the flexibility indicator of the timeline requirement."""
        self.is_flexible = is_flexible
        self.update()
    
    def validate_timeline(self) -> bool:
        """Validate that the timeline information is complete and logical."""
        try:
            start_date = parse(self.expected_start_date).date()
            end_date = parse(self.expected_end_date).date()
            
            # Validate end date is after start date
            if end_date <= start_date:
                raise ValidationException("End date must be after start date")
            
            # Validate specific days fall within start and end dates
            if self.specific_required_days:
                for day_str in self.specific_required_days:
                    day = parse(day_str).date()
                    if day < start_date or day > end_date:
                        raise ValidationException(
                            f"Specific required day {day_str} is outside the timeline range"
                        )
            
            return True
        except ValueError as e:
            raise ValidationException(f"Invalid date format: {str(e)}")
        except Exception as e:
            raise ValidationException(f"Timeline validation error: {str(e)}")
