"""
Status changed domain event.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

from .domain_event import DomainEvent


@dataclass
class StatusChangedEvent(DomainEvent):
    """Domain event raised when an opportunity status changes."""
    
    opportunity_title: str = ""
    from_status: Optional[str] = None
    to_status: str = ""
    changed_by: str = ""
    change_reason: Optional[str] = None
    change_notes: Optional[str] = None
    is_progression: bool = False
    is_regression: bool = False
    
    def __post_init__(self):
        """Initialize event after creation."""
        super().__post_init__()
        self.aggregate_type = "Opportunity"
        
        # Determine if this is progression or regression
        if self.from_status and self.to_status:
            self._analyze_status_change()
    
    @classmethod
    def create(cls, opportunity_id: str, opportunity_title: str,
               from_status: Optional[str], to_status: str, changed_by: str,
               change_reason: Optional[str] = None, change_notes: Optional[str] = None,
               user_id: Optional[str] = None) -> 'StatusChangedEvent':
        """Create a new status changed event."""
        event = cls(
            aggregate_id=opportunity_id,
            opportunity_title=opportunity_title,
            from_status=from_status,
            to_status=to_status,
            changed_by=changed_by,
            change_reason=change_reason,
            change_notes=change_notes
        )
        
        if user_id:
            event.user_id = user_id
        
        return event
    
    def get_event_data(self) -> Dict[str, Any]:
        """Get event-specific data."""
        return {
            "opportunity_title": self.opportunity_title,
            "from_status": self.from_status,
            "to_status": self.to_status,
            "changed_by": self.changed_by,
            "change_reason": self.change_reason,
            "change_notes": self.change_notes,
            "is_progression": self.is_progression,
            "is_regression": self.is_regression
        }
    
    def set_event_data(self, data: Dict[str, Any]) -> None:
        """Set event-specific data."""
        self.opportunity_title = data.get("opportunity_title", "")
        self.from_status = data.get("from_status")
        self.to_status = data.get("to_status", "")
        self.changed_by = data.get("changed_by", "")
        self.change_reason = data.get("change_reason")
        self.change_notes = data.get("change_notes")
        self.is_progression = data.get("is_progression", False)
        self.is_regression = data.get("is_regression", False)
    
    def _analyze_status_change(self) -> None:
        """Analyze the status change to determine progression/regression."""
        # Define status progression order
        status_order = [
            "Draft",
            "Submitted", 
            "Matching in Progress",
            "Matches Found",
            "Architect Selected",
            "Completed"
        ]
        
        try:
            if self.from_status and self.from_status in status_order and self.to_status in status_order:
                from_index = status_order.index(self.from_status)
                to_index = status_order.index(self.to_status)
                
                if to_index > from_index:
                    self.is_progression = True
                elif to_index < from_index:
                    self.is_regression = True
        except ValueError:
            # Status not in progression order (e.g., Cancelled)
            pass
    
    @property
    def is_initial_status(self) -> bool:
        """Check if this is the initial status setting."""
        return self.from_status is None
    
    @property
    def is_cancellation(self) -> bool:
        """Check if this represents a cancellation."""
        return self.to_status == "Cancelled"
    
    @property
    def is_reactivation(self) -> bool:
        """Check if this represents a reactivation."""
        return self.from_status == "Cancelled" and self.to_status == "Draft"
    
    @property
    def is_completion(self) -> bool:
        """Check if this represents completion."""
        return self.to_status == "Completed"
    
    @property
    def is_submission(self) -> bool:
        """Check if this represents submission for matching."""
        return self.from_status == "Draft" and self.to_status == "Submitted"
    
    @property
    def is_architect_selection(self) -> bool:
        """Check if this represents architect selection."""
        return self.to_status == "Architect Selected"
    
    @property
    def requires_notification(self) -> bool:
        """Check if this status change requires stakeholder notification."""
        notification_statuses = [
            "Submitted", "Matches Found", "Architect Selected", 
            "Completed", "Cancelled"
        ]
        return self.to_status in notification_statuses
    
    @property
    def is_milestone(self) -> bool:
        """Check if this status represents a significant milestone."""
        milestone_statuses = [
            "Submitted", "Architect Selected", "Completed"
        ]
        return self.to_status in milestone_statuses
    
    def get_notification_recipients(self) -> Dict[str, list]:
        """Get who should be notified about this status change."""
        recipients = {
            "sales_managers": [],
            "solution_architects": [],
            "administrators": []
        }
        
        # Sales manager is always notified
        recipients["sales_managers"].append(self.changed_by)
        
        # Specific notifications based on status
        if self.is_architect_selection or self.is_completion:
            recipients["solution_architects"].append("selected_architect")
        
        if self.is_cancellation and self.from_status == "Architect Selected":
            recipients["solution_architects"].append("selected_architect")
        
        if self.to_status in ["Submitted", "Completed"]:
            recipients["administrators"].append("matching_team")
        
        return recipients
    
    def get_status_change_summary(self) -> str:
        """Get a human-readable summary of the status change."""
        if self.is_initial_status:
            return f"Opportunity created with status '{self.to_status}'"
        
        summary = f"Status changed from '{self.from_status}' to '{self.to_status}'"
        
        if self.change_reason:
            summary += f" - {self.change_reason}"
        
        return summary
    
    def __str__(self) -> str:
        """String representation of the event."""
        from_str = self.from_status or "None"
        return f"StatusChanged(id={self.aggregate_id}, {from_str} -> {self.to_status})"
