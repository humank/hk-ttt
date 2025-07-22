"""
Opportunity modified domain event.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

from .domain_event import DomainEvent


@dataclass
class OpportunityModifiedEvent(DomainEvent):
    """Domain event raised when an opportunity is modified."""
    
    opportunity_title: str = ""
    modified_fields: List[str] = field(default_factory=list)
    changes_summary: List[str] = field(default_factory=list)
    previous_values: Dict[str, Any] = field(default_factory=dict)
    new_values: Dict[str, Any] = field(default_factory=dict)
    modification_reason: Optional[str] = None
    opportunity_status: str = ""
    
    def __post_init__(self):
        """Initialize event after creation."""
        super().__post_init__()
        self.aggregate_type = "Opportunity"
    
    @classmethod
    def create(cls, opportunity_id: str, opportunity_title: str, 
               modified_fields: List[str], changes_summary: List[str],
               previous_values: Dict[str, Any], new_values: Dict[str, Any],
               opportunity_status: str, modification_reason: Optional[str] = None,
               user_id: Optional[str] = None) -> 'OpportunityModifiedEvent':
        """Create a new opportunity modified event."""
        event = cls(
            aggregate_id=opportunity_id,
            opportunity_title=opportunity_title,
            modified_fields=modified_fields,
            changes_summary=changes_summary,
            previous_values=previous_values,
            new_values=new_values,
            modification_reason=modification_reason,
            opportunity_status=opportunity_status
        )
        
        if user_id:
            event.user_id = user_id
        
        return event
    
    def get_event_data(self) -> Dict[str, Any]:
        """Get event-specific data."""
        return {
            "opportunity_title": self.opportunity_title,
            "modified_fields": self.modified_fields,
            "changes_summary": self.changes_summary,
            "previous_values": self.previous_values,
            "new_values": self.new_values,
            "modification_reason": self.modification_reason,
            "opportunity_status": self.opportunity_status
        }
    
    def set_event_data(self, data: Dict[str, Any]) -> None:
        """Set event-specific data."""
        self.opportunity_title = data.get("opportunity_title", "")
        self.modified_fields = data.get("modified_fields", [])
        self.changes_summary = data.get("changes_summary", [])
        self.previous_values = data.get("previous_values", {})
        self.new_values = data.get("new_values", {})
        self.modification_reason = data.get("modification_reason")
        self.opportunity_status = data.get("opportunity_status", "")
    
    @property
    def is_significant_change(self) -> bool:
        """Check if this represents a significant change."""
        significant_fields = [
            "priority", "annual_recurring_revenue", "timeline_specification",
            "skill_requirements", "problem_statement"
        ]
        return any(field in self.modified_fields for field in significant_fields)
    
    @property
    def is_basic_info_change(self) -> bool:
        """Check if this is a basic information change."""
        basic_fields = ["title", "description", "notes"]
        return all(field in basic_fields for field in self.modified_fields)
    
    @property
    def is_requirements_change(self) -> bool:
        """Check if this involves requirements changes."""
        requirements_fields = [
            "skill_requirements", "timeline_specification", 
            "geographic_requirement", "language_requirements"
        ]
        return any(field in self.modified_fields for field in requirements_fields)
    
    def get_field_change(self, field_name: str) -> Optional[Dict[str, Any]]:
        """Get the change details for a specific field."""
        if field_name not in self.modified_fields:
            return None
        
        return {
            "field": field_name,
            "previous_value": self.previous_values.get(field_name),
            "new_value": self.new_values.get(field_name)
        }
    
    def has_field_change(self, field_name: str) -> bool:
        """Check if a specific field was changed."""
        return field_name in self.modified_fields
    
    def __str__(self) -> str:
        """String representation of the event."""
        fields_str = ", ".join(self.modified_fields)
        return f"OpportunityModified(id={self.aggregate_id}, fields=[{fields_str}])"
