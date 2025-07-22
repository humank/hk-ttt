"""
Geographic requirement value object for opportunity location specifications.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass(frozen=True)
class GeographicRequirement:
    """Value object representing geographic requirements for an opportunity."""
    
    preferred_locations: List[str]
    remote_work_allowed: bool = True
    travel_required: bool = False
    travel_percentage: Optional[int] = None  # 0-100
    time_zone_preference: Optional[str] = None
    country_restrictions: Optional[List[str]] = None
    notes: Optional[str] = None
    
    def __post_init__(self):
        """Validate geographic requirement after initialization."""
        if not self.preferred_locations:
            raise ValueError("At least one preferred location must be specified")
        
        if self.travel_percentage is not None:
            if not (0 <= self.travel_percentage <= 100):
                raise ValueError("Travel percentage must be between 0 and 100")
        
        if self.travel_required and self.travel_percentage is None:
            raise ValueError("Travel percentage must be specified when travel is required")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert geographic requirement to dictionary representation."""
        return {
            "preferred_locations": self.preferred_locations,
            "remote_work_allowed": self.remote_work_allowed,
            "travel_required": self.travel_required,
            "travel_percentage": self.travel_percentage,
            "time_zone_preference": self.time_zone_preference,
            "country_restrictions": self.country_restrictions,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GeographicRequirement':
        """Create GeographicRequirement from dictionary."""
        return cls(
            preferred_locations=data["preferred_locations"],
            remote_work_allowed=data.get("remote_work_allowed", True),
            travel_required=data.get("travel_required", False),
            travel_percentage=data.get("travel_percentage"),
            time_zone_preference=data.get("time_zone_preference"),
            country_restrictions=data.get("country_restrictions"),
            notes=data.get("notes")
        )
    
    def allows_location(self, location: str) -> bool:
        """Check if a location is allowed based on requirements."""
        if self.country_restrictions and location in self.country_restrictions:
            return False
        
        if not self.remote_work_allowed:
            return location in self.preferred_locations
        
        return True
    
    def matches_location_preference(self, location: str) -> bool:
        """Check if a location matches the preference."""
        return location in self.preferred_locations
    
    @property
    def is_location_flexible(self) -> bool:
        """Check if location requirements are flexible."""
        return self.remote_work_allowed and not self.travel_required
