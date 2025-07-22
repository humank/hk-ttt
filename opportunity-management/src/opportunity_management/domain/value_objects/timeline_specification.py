"""
Timeline specification value object for opportunity timeline requirements.
"""

from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, Any, Optional, List
from ..enums.timeline_flexibility import TimelineFlexibility


@dataclass(frozen=True)
class TimelineSpecification:
    """Value object representing timeline requirements for an opportunity."""
    
    expected_start_date: date
    expected_duration_days: int
    expected_end_date: Optional[date] = None
    flexibility: TimelineFlexibility = TimelineFlexibility.FLEXIBLE
    specific_days_required: Optional[List[str]] = None  # e.g., ["Monday", "Wednesday", "Friday"]
    notes: Optional[str] = None
    
    def __post_init__(self):
        """Validate timeline specification after initialization."""
        if self.expected_start_date < date.today():
            raise ValueError("Expected start date cannot be in the past")
        
        if self.expected_duration_days <= 0:
            raise ValueError("Expected duration must be positive")
        
        if self.expected_end_date:
            if self.expected_end_date <= self.expected_start_date:
                raise ValueError("Expected end date must be after start date")
        
        if self.specific_days_required:
            valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            for day in self.specific_days_required:
                if day not in valid_days:
                    raise ValueError(f"Invalid day: {day}")
    
    @property
    def calculated_end_date(self) -> date:
        """Calculate end date based on start date and duration."""
        if self.expected_end_date:
            return self.expected_end_date
        
        from datetime import timedelta
        return self.expected_start_date + timedelta(days=self.expected_duration_days)
    
    @property
    def total_duration_days(self) -> int:
        """Get total duration in days."""
        if self.expected_end_date:
            return (self.expected_end_date - self.expected_start_date).days
        return self.expected_duration_days
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert timeline specification to dictionary representation."""
        return {
            "expected_start_date": self.expected_start_date.isoformat(),
            "expected_duration_days": self.expected_duration_days,
            "expected_end_date": self.expected_end_date.isoformat() if self.expected_end_date else None,
            "flexibility": self.flexibility.value,
            "specific_days_required": self.specific_days_required,
            "notes": self.notes,
            "calculated_end_date": self.calculated_end_date.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TimelineSpecification':
        """Create TimelineSpecification from dictionary."""
        return cls(
            expected_start_date=date.fromisoformat(data["expected_start_date"]),
            expected_duration_days=data["expected_duration_days"],
            expected_end_date=date.fromisoformat(data["expected_end_date"]) if data.get("expected_end_date") else None,
            flexibility=TimelineFlexibility.from_string(data["flexibility"]),
            specific_days_required=data.get("specific_days_required"),
            notes=data.get("notes")
        )
    
    def overlaps_with(self, other: 'TimelineSpecification') -> bool:
        """Check if this timeline overlaps with another timeline."""
        return not (self.calculated_end_date < other.expected_start_date or 
                   other.calculated_end_date < self.expected_start_date)
    
    def is_within_range(self, start_date: date, end_date: date) -> bool:
        """Check if this timeline is within a given date range."""
        return (self.expected_start_date >= start_date and 
                self.calculated_end_date <= end_date)
