"""
Base domain event class for all domain events in the system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
import uuid


@dataclass
class DomainEvent:
    """Base class for all domain events."""
    
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = field(init=False)
    aggregate_id: str = ""
    aggregate_type: str = ""
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None
    user_id: Optional[str] = None
    
    def __post_init__(self):
        """Set event type based on class name."""
        if not self.event_type:
            self.event_type = self.__class__.__name__
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert domain event to dictionary representation."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "occurred_at": self.occurred_at.isoformat(),
            "version": self.version,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "user_id": self.user_id,
            "event_data": self.get_event_data()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DomainEvent':
        """Create domain event from dictionary."""
        event = cls()
        event.event_id = data["event_id"]
        event.event_type = data["event_type"]
        event.aggregate_id = data["aggregate_id"]
        event.aggregate_type = data["aggregate_type"]
        event.occurred_at = datetime.fromisoformat(data["occurred_at"])
        event.version = data["version"]
        event.correlation_id = data.get("correlation_id")
        event.causation_id = data.get("causation_id")
        event.user_id = data.get("user_id")
        
        # Set event-specific data
        if "event_data" in data:
            event.set_event_data(data["event_data"])
        
        return event
    
    def get_event_data(self) -> Dict[str, Any]:
        """Get event-specific data. Override in subclasses."""
        return {}
    
    def set_event_data(self, data: Dict[str, Any]) -> None:
        """Set event-specific data. Override in subclasses."""
        pass
    
    def with_correlation_id(self, correlation_id: str) -> 'DomainEvent':
        """Set correlation ID for event tracing."""
        self.correlation_id = correlation_id
        return self
    
    def with_causation_id(self, causation_id: str) -> 'DomainEvent':
        """Set causation ID for event tracing."""
        self.causation_id = causation_id
        return self
    
    def with_user_id(self, user_id: str) -> 'DomainEvent':
        """Set user ID who triggered the event."""
        self.user_id = user_id
        return self
    
    @property
    def is_recent(self) -> bool:
        """Check if event occurred recently (within last hour)."""
        from datetime import timedelta
        return (datetime.utcnow() - self.occurred_at) < timedelta(hours=1)
    
    def __str__(self) -> str:
        """String representation of domain event."""
        return f"{self.event_type}(id={self.event_id}, aggregate={self.aggregate_id})"
