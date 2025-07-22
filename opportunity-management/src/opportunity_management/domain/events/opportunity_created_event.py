"""
Opportunity created domain event.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from decimal import Decimal

from .domain_event import DomainEvent


@dataclass
class OpportunityCreatedEvent(DomainEvent):
    """Domain event raised when a new opportunity is created."""
    
    opportunity_title: str = ""
    customer_id: str = ""
    sales_manager_id: str = ""
    annual_recurring_revenue: Optional[Decimal] = None
    priority: str = ""
    
    def __post_init__(self):
        """Initialize event after creation."""
        super().__post_init__()
        self.aggregate_type = "Opportunity"
    
    @classmethod
    def create(cls, opportunity_id: str, opportunity_title: str, customer_id: str,
               sales_manager_id: str, annual_recurring_revenue: Decimal, 
               priority: str, user_id: Optional[str] = None) -> 'OpportunityCreatedEvent':
        """Create a new opportunity created event."""
        event = cls(
            aggregate_id=opportunity_id,
            opportunity_title=opportunity_title,
            customer_id=customer_id,
            sales_manager_id=sales_manager_id,
            annual_recurring_revenue=annual_recurring_revenue,
            priority=priority
        )
        
        if user_id:
            event.user_id = user_id
        
        return event
    
    def get_event_data(self) -> Dict[str, Any]:
        """Get event-specific data."""
        return {
            "opportunity_title": self.opportunity_title,
            "customer_id": self.customer_id,
            "sales_manager_id": self.sales_manager_id,
            "annual_recurring_revenue": str(self.annual_recurring_revenue) if self.annual_recurring_revenue else None,
            "priority": self.priority
        }
    
    def set_event_data(self, data: Dict[str, Any]) -> None:
        """Set event-specific data."""
        self.opportunity_title = data.get("opportunity_title", "")
        self.customer_id = data.get("customer_id", "")
        self.sales_manager_id = data.get("sales_manager_id", "")
        
        arr_str = data.get("annual_recurring_revenue")
        if arr_str:
            self.annual_recurring_revenue = Decimal(arr_str)
        
        self.priority = data.get("priority", "")
    
    @property
    def is_high_value(self) -> bool:
        """Check if this is a high-value opportunity."""
        if self.annual_recurring_revenue:
            return self.annual_recurring_revenue >= Decimal('500000')
        return False
    
    @property
    def is_high_priority(self) -> bool:
        """Check if this is a high-priority opportunity."""
        return self.priority in ["High", "Critical"]
    
    def __str__(self) -> str:
        """String representation of the event."""
        return f"OpportunityCreated(id={self.aggregate_id}, title='{self.opportunity_title}', priority={self.priority})"
