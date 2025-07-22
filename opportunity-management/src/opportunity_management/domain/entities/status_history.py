"""
Status history entity for tracking opportunity status changes.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from .base_entity import BaseEntity
from ..enums.status import OpportunityStatus


@dataclass
class StatusHistory(BaseEntity):
    """Entity representing a status change in an opportunity's lifecycle."""
    
    opportunity_id: str = ""
    from_status: Optional[OpportunityStatus] = None
    to_status: OpportunityStatus = OpportunityStatus.DRAFT
    changed_by: str = ""
    change_reason: Optional[str] = None
    notes: Optional[str] = None
    
    def __post_init__(self):
        """Validate status history after initialization."""
        super().__post_init__()
        
        if not self.opportunity_id or not self.opportunity_id.strip():
            raise ValueError("Opportunity ID cannot be empty")
        
        if not self.changed_by or not self.changed_by.strip():
            raise ValueError("Changed by cannot be empty")
        
        # Validate status transition if from_status is provided
        if self.from_status and not self.from_status.can_transition_to(self.to_status):
            raise ValueError(f"Invalid status transition from {self.from_status} to {self.to_status}")
    
    @classmethod
    def create_initial_status(cls, opportunity_id: str, initial_status: OpportunityStatus, 
                            created_by: str, notes: Optional[str] = None) -> 'StatusHistory':
        """Create the initial status history entry for a new opportunity."""
        return cls(
            opportunity_id=opportunity_id,
            from_status=None,
            to_status=initial_status,
            changed_by=created_by,
            change_reason="Initial status",
            notes=notes
        )
    
    @classmethod
    def create_status_change(cls, opportunity_id: str, from_status: OpportunityStatus, 
                           to_status: OpportunityStatus, changed_by: str, 
                           reason: Optional[str] = None, notes: Optional[str] = None) -> 'StatusHistory':
        """Create a status change history entry."""
        return cls(
            opportunity_id=opportunity_id,
            from_status=from_status,
            to_status=to_status,
            changed_by=changed_by,
            change_reason=reason,
            notes=notes
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert status history to dictionary representation."""
        base_dict = super().to_dict()
        base_dict.update({
            "opportunity_id": self.opportunity_id,
            "from_status": self.from_status.value if self.from_status else None,
            "to_status": self.to_status.value,
            "changed_by": self.changed_by,
            "change_reason": self.change_reason,
            "notes": self.notes
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StatusHistory':
        """Create StatusHistory from dictionary."""
        from_status = None
        if data.get("from_status"):
            from_status = OpportunityStatus.from_string(data["from_status"])
        
        status_history = cls(
            opportunity_id=data["opportunity_id"],
            from_status=from_status,
            to_status=OpportunityStatus.from_string(data["to_status"]),
            changed_by=data["changed_by"],
            change_reason=data.get("change_reason"),
            notes=data.get("notes")
        )
        status_history.update_from_dict(data)
        return status_history
    
    @property
    def is_initial_status(self) -> bool:
        """Check if this is the initial status entry."""
        return self.from_status is None
    
    @property
    def is_status_progression(self) -> bool:
        """Check if this represents forward progression in the workflow."""
        if self.from_status is None:
            return True
        
        # Define status progression order
        progression_order = [
            OpportunityStatus.DRAFT,
            OpportunityStatus.SUBMITTED,
            OpportunityStatus.MATCHING_IN_PROGRESS,
            OpportunityStatus.MATCHES_FOUND,
            OpportunityStatus.ARCHITECT_SELECTED,
            OpportunityStatus.COMPLETED
        ]
        
        try:
            from_index = progression_order.index(self.from_status)
            to_index = progression_order.index(self.to_status)
            return to_index > from_index
        except ValueError:
            # Status not in progression order (e.g., CANCELLED)
            return False
    
    @property
    def is_cancellation(self) -> bool:
        """Check if this represents a cancellation."""
        return self.to_status == OpportunityStatus.CANCELLED
    
    @property
    def is_reactivation(self) -> bool:
        """Check if this represents a reactivation from cancelled status."""
        return (self.from_status == OpportunityStatus.CANCELLED and 
                self.to_status == OpportunityStatus.DRAFT)
    
    def __str__(self) -> str:
        """String representation of status history."""
        from_str = self.from_status.value if self.from_status else "None"
        return f"StatusHistory(opportunity={self.opportunity_id}, {from_str} -> {self.to_status.value})"
