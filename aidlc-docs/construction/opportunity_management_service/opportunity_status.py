"""
OpportunityStatus entity for the Opportunity Management Service.
"""

import uuid
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from datetime import datetime

from .base_entity import BaseEntity
from .enums import OpportunityStatus as StatusEnum

@dataclass
class OpportunityStatus(BaseEntity):
    """OpportunityStatus entity representing the current status and status history of an opportunity."""
    
    opportunity_id: uuid.UUID
    status: StatusEnum
    changed_by: uuid.UUID
    changed_at: datetime = field(default_factory=datetime.now)
    reason: Optional[str] = None
    
    @staticmethod
    def create_status_record(opportunity_id: uuid.UUID, status: StatusEnum, 
                            changed_by: uuid.UUID, reason: Optional[str] = None) -> 'OpportunityStatus':
        """Create a new status record."""
        return OpportunityStatus(
            opportunity_id=opportunity_id,
            status=status,
            changed_by=changed_by,
            reason=reason
        )
    
    @staticmethod
    def is_valid_transition(current_status: StatusEnum, new_status: StatusEnum) -> bool:
        """Validate if the transition from current to new status is allowed."""
        # Define valid transitions
        valid_transitions = {
            StatusEnum.DRAFT: [StatusEnum.SUBMITTED, StatusEnum.CANCELLED],
            StatusEnum.SUBMITTED: [StatusEnum.MATCHING_IN_PROGRESS, StatusEnum.CANCELLED],
            StatusEnum.MATCHING_IN_PROGRESS: [StatusEnum.MATCHES_FOUND, StatusEnum.CANCELLED],
            StatusEnum.MATCHES_FOUND: [StatusEnum.ARCHITECT_SELECTED, StatusEnum.CANCELLED],
            StatusEnum.ARCHITECT_SELECTED: [StatusEnum.COMPLETED, StatusEnum.CANCELLED],
            StatusEnum.COMPLETED: [],  # No transitions from Completed
            StatusEnum.CANCELLED: []   # No transitions from Cancelled (reactivation is handled separately)
        }
        
        return new_status in valid_transitions.get(current_status, [])
