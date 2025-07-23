"""
ChangeRecord entity for the Opportunity Management Service.
"""

import uuid
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from datetime import datetime

from .base_entity import BaseEntity

@dataclass
class ChangeRecord(BaseEntity):
    """ChangeRecord entity representing a change made to an opportunity for audit purposes."""
    
    opportunity_id: uuid.UUID
    changed_by: uuid.UUID
    field_changed: str
    reason: str
    changed_at: datetime = field(default_factory=datetime.now)
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    
    @staticmethod
    def create_change_record(opportunity_id: uuid.UUID, changed_by: uuid.UUID, 
                           field_changed: str, reason: str, old_value: Optional[str] = None, 
                           new_value: Optional[str] = None) -> 'ChangeRecord':
        """Create a new change record."""
        return ChangeRecord(
            opportunity_id=opportunity_id,
            changed_by=changed_by,
            field_changed=field_changed,
            reason=reason,
            old_value=old_value,
            new_value=new_value
        )
