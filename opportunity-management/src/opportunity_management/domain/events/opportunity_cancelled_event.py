"""
Opportunity cancelled domain event.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import date

from .domain_event import DomainEvent


@dataclass
class OpportunityCancelledEvent(DomainEvent):
    """Domain event raised when an opportunity is cancelled."""
    
    opportunity_title: str = ""
    previous_status: str = ""
    cancellation_reason: str = ""
    cancellation_date: Optional[date] = None
    cancelled_by: str = ""
    notes: Optional[str] = None
    selected_architect_id: Optional[str] = None
    can_be_reactivated: bool = True
    reactivation_deadline: Optional[date] = None
    
    def __post_init__(self):
        """Initialize event after creation."""
        super().__post_init__()
        self.aggregate_type = "Opportunity"
    
    @classmethod
    def create(cls, opportunity_id: str, opportunity_title: str, previous_status: str,
               cancellation_reason: str, cancelled_by: str, 
               cancellation_date: Optional[date] = None,
               notes: Optional[str] = None, selected_architect_id: Optional[str] = None,
               user_id: Optional[str] = None) -> 'OpportunityCancelledEvent':
        """Create a new opportunity cancelled event."""
        if cancellation_date is None:
            cancellation_date = date.today()
        
        # Calculate reactivation deadline (90 days from cancellation)
        from datetime import timedelta
        reactivation_deadline = cancellation_date + timedelta(days=90)
        
        event = cls(
            aggregate_id=opportunity_id,
            opportunity_title=opportunity_title,
            previous_status=previous_status,
            cancellation_reason=cancellation_reason,
            cancellation_date=cancellation_date,
            cancelled_by=cancelled_by,
            notes=notes,
            selected_architect_id=selected_architect_id,
            reactivation_deadline=reactivation_deadline
        )
        
        if user_id:
            event.user_id = user_id
        
        return event
    
    def get_event_data(self) -> Dict[str, Any]:
        """Get event-specific data."""
        return {
            "opportunity_title": self.opportunity_title,
            "previous_status": self.previous_status,
            "cancellation_reason": self.cancellation_reason,
            "cancellation_date": self.cancellation_date.isoformat() if self.cancellation_date else None,
            "cancelled_by": self.cancelled_by,
            "notes": self.notes,
            "selected_architect_id": self.selected_architect_id,
            "can_be_reactivated": self.can_be_reactivated,
            "reactivation_deadline": self.reactivation_deadline.isoformat() if self.reactivation_deadline else None
        }
    
    def set_event_data(self, data: Dict[str, Any]) -> None:
        """Set event-specific data."""
        self.opportunity_title = data.get("opportunity_title", "")
        self.previous_status = data.get("previous_status", "")
        self.cancellation_reason = data.get("cancellation_reason", "")
        self.cancelled_by = data.get("cancelled_by", "")
        self.notes = data.get("notes")
        self.selected_architect_id = data.get("selected_architect_id")
        self.can_be_reactivated = data.get("can_be_reactivated", True)
        
        cancellation_date_str = data.get("cancellation_date")
        if cancellation_date_str:
            self.cancellation_date = date.fromisoformat(cancellation_date_str)
        
        reactivation_deadline_str = data.get("reactivation_deadline")
        if reactivation_deadline_str:
            self.reactivation_deadline = date.fromisoformat(reactivation_deadline_str)
    
    @property
    def was_in_progress(self) -> bool:
        """Check if opportunity was in progress when cancelled."""
        in_progress_statuses = [
            "Matching in Progress", "Matches Found", "Architect Selected"
        ]
        return self.previous_status in in_progress_statuses
    
    @property
    def had_selected_architect(self) -> bool:
        """Check if opportunity had a selected architect."""
        return self.selected_architect_id is not None
    
    @property
    def days_until_reactivation_deadline(self) -> Optional[int]:
        """Get days remaining until reactivation deadline."""
        if not self.reactivation_deadline:
            return None
        
        today = date.today()
        if today > self.reactivation_deadline:
            return 0  # Deadline passed
        
        return (self.reactivation_deadline - today).days
    
    @property
    def is_reactivation_expired(self) -> bool:
        """Check if reactivation period has expired."""
        if not self.reactivation_deadline:
            return False
        
        return date.today() > self.reactivation_deadline
    
    def get_impact_assessment(self) -> Dict[str, Any]:
        """Get impact assessment of the cancellation."""
        impact = {
            "severity": "Low",
            "affected_parties": ["Sales Manager"],
            "requires_notification": False,
            "financial_impact": False
        }
        
        # Assess severity based on status
        if self.previous_status == "Architect Selected":
            impact["severity"] = "High"
            impact["affected_parties"].extend(["Solution Architect", "Customer"])
            impact["requires_notification"] = True
        elif self.previous_status in ["Matching in Progress", "Matches Found"]:
            impact["severity"] = "Medium"
            impact["requires_notification"] = True
        
        # Check for financial impact
        if self.had_selected_architect:
            impact["financial_impact"] = True
        
        return impact
    
    def __str__(self) -> str:
        """String representation of the event."""
        return f"OpportunityCancelled(id={self.aggregate_id}, reason='{self.cancellation_reason}', by={self.cancelled_by})"
