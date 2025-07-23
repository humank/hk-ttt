"""
Opportunity entity for the Opportunity Management Service.
"""

import uuid
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from .base_entity import BaseEntity
from .enums import Priority, OpportunityStatus
from .value_objects import GeographicRequirements
from .common import ValidationException, OperationNotAllowedException, EventPublisher

@dataclass
class Opportunity(BaseEntity):
    """Opportunity entity representing a customer opportunity that requires a Solution Architect."""
    
    title: str
    customer_id: uuid.UUID
    customer_name: str
    sales_manager_id: uuid.UUID
    description: str
    priority: Priority
    annual_recurring_revenue: float
    geographic_requirements: GeographicRequirements
    status: OpportunityStatus = OpportunityStatus.DRAFT
    submitted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    reactivation_deadline: Optional[datetime] = None
    
    @staticmethod
    def create_opportunity(title: str, customer_id: uuid.UUID, customer_name: str,
                         sales_manager_id: uuid.UUID, description: str, priority: Priority,
                         annual_recurring_revenue: float, geographic_requirements: GeographicRequirements) -> 'Opportunity':
        """Create a new opportunity."""
        # Validate required fields
        if not title or not description:
            raise ValidationException("Title and description are required")
        
        opportunity = Opportunity(
            title=title,
            customer_id=customer_id,
            customer_name=customer_name,
            sales_manager_id=sales_manager_id,
            description=description,
            priority=priority,
            annual_recurring_revenue=annual_recurring_revenue,
            geographic_requirements=geographic_requirements
        )
        
        return opportunity
    
    def submit_opportunity(self, problem_statement_validator, skill_requirements_validator, 
                          timeline_validator) -> None:
        """Submit the opportunity for matching."""
        # Validate current status
        if self.status != OpportunityStatus.DRAFT:
            raise OperationNotAllowedException("Only opportunities in Draft status can be submitted")
        
        # Validate all required components
        problem_statement_validator(self.id)
        skill_requirements_validator(self.id)
        timeline_validator(self.id)
        
        # Update status and submission timestamp
        self.status = OpportunityStatus.SUBMITTED
        self.submitted_at = datetime.now()
        self.update()
        
        # Publish event for matching process
        EventPublisher.publish("opportunity.submitted", {"opportunity_id": str(self.id)})
    
    def update_opportunity(self, field: str, new_value: Any, reason: str, changed_by: uuid.UUID,
                          change_record_creator) -> None:
        """Update an opportunity field."""
        # Validate current status
        if self.status in [OpportunityStatus.ARCHITECT_SELECTED, OpportunityStatus.COMPLETED]:
            raise OperationNotAllowedException(
                "Opportunities with Architect Selected or Completed status cannot be modified"
            )
        
        # Get old value
        old_value = getattr(self, field, None)
        old_value_str = str(old_value) if old_value is not None else None
        
        # Update field
        setattr(self, field, new_value)
        self.update()
        
        # Create change record
        new_value_str = str(new_value) if new_value is not None else None
        change_record_creator(
            self.id, changed_by, field, reason, old_value_str, new_value_str
        )
        
        # Publish event
        EventPublisher.publish("opportunity.updated", {
            "opportunity_id": str(self.id),
            "field": field,
            "old_value": old_value_str,
            "new_value": new_value_str
        })
    
    def cancel_opportunity(self, reason: str, changed_by: uuid.UUID, 
                          status_record_creator, change_record_creator) -> None:
        """Cancel the opportunity."""
        # Validate current status
        if self.status == OpportunityStatus.COMPLETED:
            raise OperationNotAllowedException("Completed opportunities cannot be cancelled")
        
        if not reason:
            raise ValidationException("Cancellation reason is required")
        
        # Store previous status for potential reactivation
        previous_status = self.status
        
        # Update status and cancellation information
        self.status = OpportunityStatus.CANCELLED
        self.cancelled_at = datetime.now()
        self.cancellation_reason = reason
        self.reactivation_deadline = datetime.now() + timedelta(days=90)
        self.update()
        
        # Create status record
        status_record_creator(self.id, OpportunityStatus.CANCELLED, changed_by, reason)
        
        # Create change record
        change_record_creator(
            self.id, changed_by, "status", reason, 
            previous_status.value, OpportunityStatus.CANCELLED.value
        )
        
        # Publish event
        EventPublisher.publish("opportunity.cancelled", {
            "opportunity_id": str(self.id),
            "reason": reason
        })
    
    def reactivate_opportunity(self, changed_by: uuid.UUID, status_record_creator, 
                             change_record_creator) -> None:
        """Reactivate a cancelled opportunity."""
        # Validate current status
        if self.status != OpportunityStatus.CANCELLED:
            raise OperationNotAllowedException("Only cancelled opportunities can be reactivated")
        
        # Validate reactivation deadline
        if not self.reactivation_deadline or datetime.now() > self.reactivation_deadline:
            raise OperationNotAllowedException(
                "Opportunity cannot be reactivated after the reactivation deadline"
            )
        
        # Determine previous status (default to DRAFT if unknown)
        # In a real implementation, we would store the previous status
        previous_status = OpportunityStatus.DRAFT
        
        # Update status and clear cancellation information
        self.status = previous_status
        self.cancelled_at = None
        self.cancellation_reason = None
        self.reactivation_deadline = None
        self.update()
        
        # Create status record
        status_record_creator(self.id, previous_status, changed_by, "Opportunity reactivated")
        
        # Create change record
        change_record_creator(
            self.id, changed_by, "status", "Opportunity reactivated", 
            OpportunityStatus.CANCELLED.value, previous_status.value
        )
        
        # Publish event
        EventPublisher.publish("opportunity.reactivated", {
            "opportunity_id": str(self.id)
        })
    
    def get_status(self) -> OpportunityStatus:
        """Get the current status of the opportunity."""
        return self.status
