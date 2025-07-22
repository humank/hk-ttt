"""
Opportunity status enumeration for tracking opportunity lifecycle.
"""

from enum import Enum
from typing import Dict, Any, List


class OpportunityStatus(Enum):
    """Enumeration for opportunity status throughout its lifecycle."""
    
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    MATCHING_IN_PROGRESS = "Matching in Progress"
    MATCHES_FOUND = "Matches Found"
    ARCHITECT_SELECTED = "Architect Selected"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    
    def __str__(self) -> str:
        """Return string representation of status."""
        return self.value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert status to dictionary representation."""
        return {"status": self.value}
    
    @classmethod
    def from_string(cls, status_str: str) -> 'OpportunityStatus':
        """Create OpportunityStatus from string value."""
        for status in cls:
            if status.value.lower() == status_str.lower():
                return status
        raise ValueError(f"Invalid status: {status_str}")
    
    def can_transition_to(self, new_status: 'OpportunityStatus') -> bool:
        """Check if transition to new status is allowed."""
        valid_transitions = {
            OpportunityStatus.DRAFT: [
                OpportunityStatus.SUBMITTED,
                OpportunityStatus.CANCELLED
            ],
            OpportunityStatus.SUBMITTED: [
                OpportunityStatus.MATCHING_IN_PROGRESS,
                OpportunityStatus.CANCELLED
            ],
            OpportunityStatus.MATCHING_IN_PROGRESS: [
                OpportunityStatus.MATCHES_FOUND,
                OpportunityStatus.CANCELLED
            ],
            OpportunityStatus.MATCHES_FOUND: [
                OpportunityStatus.ARCHITECT_SELECTED,
                OpportunityStatus.CANCELLED
            ],
            OpportunityStatus.ARCHITECT_SELECTED: [
                OpportunityStatus.COMPLETED,
                OpportunityStatus.CANCELLED
            ],
            OpportunityStatus.COMPLETED: [],
            OpportunityStatus.CANCELLED: [OpportunityStatus.DRAFT]  # Reactivation
        }
        
        return new_status in valid_transitions.get(self, [])
    
    @property
    def is_modifiable(self) -> bool:
        """Check if opportunity can be modified in this status."""
        return self in [
            OpportunityStatus.DRAFT,
            OpportunityStatus.SUBMITTED
        ]
    
    @property
    def is_final(self) -> bool:
        """Check if this is a final status."""
        return self in [
            OpportunityStatus.COMPLETED,
            OpportunityStatus.CANCELLED
        ]
