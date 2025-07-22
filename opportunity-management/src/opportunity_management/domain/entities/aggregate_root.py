"""
Aggregate root class extending base entity with domain event support.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from .base_entity import BaseEntity


@dataclass
class AggregateRoot(BaseEntity):
    """Base class for aggregate roots with domain event support."""
    
    _domain_events: List['DomainEvent'] = field(default_factory=list, init=False)
    
    def add_domain_event(self, event: 'DomainEvent') -> None:
        """Add a domain event to be published."""
        self._domain_events.append(event)
    
    def get_domain_events(self) -> List['DomainEvent']:
        """Get all domain events for this aggregate."""
        return self._domain_events.copy()
    
    def clear_domain_events(self) -> None:
        """Clear all domain events after they have been published."""
        self._domain_events.clear()
    
    def has_domain_events(self) -> bool:
        """Check if there are any unpublished domain events."""
        return len(self._domain_events) > 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert aggregate root to dictionary representation."""
        base_dict = super().to_dict()
        base_dict["has_domain_events"] = self.has_domain_events()
        base_dict["domain_events_count"] = len(self._domain_events)
        return base_dict
    
    def mark_events_as_committed(self) -> None:
        """Mark domain events as committed and clear them."""
        self.clear_domain_events()
        self.update_timestamp()


# Forward declaration for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from domain_event import DomainEvent
