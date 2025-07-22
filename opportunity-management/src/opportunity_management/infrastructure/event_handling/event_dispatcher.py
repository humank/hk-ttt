"""
Event dispatcher for handling domain events with simple dependency injection.
"""

from typing import Dict, List, Callable, Any, Optional
import logging
from datetime import datetime

from ...domain.events.domain_event import DomainEvent


class EventHandler:
    """Base class for event handlers."""
    
    def handle(self, event: DomainEvent) -> None:
        """Handle the domain event. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement handle method")
    
    def can_handle(self, event_type: str) -> bool:
        """Check if this handler can handle the event type."""
        return False


class EventDispatcher:
    """Simple event dispatcher for domain events."""
    
    def __init__(self):
        """Initialize the event dispatcher."""
        self.handlers: Dict[str, List[EventHandler]] = {}
        self.logger = logging.getLogger(__name__)
        self.event_history: List[Dict[str, Any]] = []
        self.max_history_size = 1000
    
    def register_handler(self, event_type: str, handler: EventHandler) -> None:
        """Register an event handler for a specific event type."""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        
        self.handlers[event_type].append(handler)
        self.logger.info(f"Registered handler {handler.__class__.__name__} for event type {event_type}")
    
    def register_function_handler(self, event_type: str, handler_func: Callable[[DomainEvent], None]) -> None:
        """Register a function as an event handler."""
        class FunctionHandler(EventHandler):
            def __init__(self, func):
                self.func = func
            
            def handle(self, event: DomainEvent) -> None:
                self.func(event)
            
            def can_handle(self, event_type: str) -> bool:
                return True
        
        self.register_handler(event_type, FunctionHandler(handler_func))
    
    def dispatch(self, event: DomainEvent) -> None:
        """Dispatch a domain event to all registered handlers."""
        self.logger.info(f"Dispatching event: {event}")
        
        # Record event in history
        self._record_event(event)
        
        # Get handlers for this event type
        handlers = self.handlers.get(event.event_type, [])
        
        if not handlers:
            self.logger.warning(f"No handlers registered for event type: {event.event_type}")
            return
        
        # Dispatch to all handlers
        for handler in handlers:
            try:
                if handler.can_handle(event.event_type):
                    handler.handle(event)
                    self.logger.debug(f"Event handled by {handler.__class__.__name__}")
            except Exception as e:
                self.logger.error(f"Error handling event {event.event_id} with handler {handler.__class__.__name__}: {str(e)}")
                # Continue with other handlers even if one fails
    
    def dispatch_events(self, events: List[DomainEvent]) -> None:
        """Dispatch multiple domain events."""
        for event in events:
            self.dispatch(event)
    
    def get_handlers(self, event_type: str) -> List[EventHandler]:
        """Get all handlers for a specific event type."""
        return self.handlers.get(event_type, []).copy()
    
    def remove_handler(self, event_type: str, handler: EventHandler) -> bool:
        """Remove a specific handler for an event type."""
        if event_type in self.handlers:
            try:
                self.handlers[event_type].remove(handler)
                self.logger.info(f"Removed handler {handler.__class__.__name__} for event type {event_type}")
                return True
            except ValueError:
                pass
        return False
    
    def clear_handlers(self, event_type: Optional[str] = None) -> None:
        """Clear handlers for a specific event type or all handlers."""
        if event_type:
            if event_type in self.handlers:
                del self.handlers[event_type]
                self.logger.info(f"Cleared all handlers for event type {event_type}")
        else:
            self.handlers.clear()
            self.logger.info("Cleared all event handlers")
    
    def get_event_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get event history with optional limit."""
        if limit:
            return self.event_history[-limit:]
        return self.event_history.copy()
    
    def get_events_by_type(self, event_type: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get events of a specific type from history."""
        filtered_events = [
            event for event in self.event_history 
            if event["event_type"] == event_type
        ]
        
        if limit:
            return filtered_events[-limit:]
        return filtered_events
    
    def get_events_by_aggregate(self, aggregate_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get events for a specific aggregate from history."""
        filtered_events = [
            event for event in self.event_history 
            if event["aggregate_id"] == aggregate_id
        ]
        
        if limit:
            return filtered_events[-limit:]
        return filtered_events
    
    def clear_event_history(self) -> None:
        """Clear the event history."""
        self.event_history.clear()
        self.logger.info("Event history cleared")
    
    def _record_event(self, event: DomainEvent) -> None:
        """Record event in history."""
        event_record = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "aggregate_id": event.aggregate_id,
            "aggregate_type": event.aggregate_type,
            "occurred_at": event.occurred_at.isoformat(),
            "dispatched_at": datetime.utcnow().isoformat(),
            "user_id": event.user_id,
            "correlation_id": event.correlation_id
        }
        
        self.event_history.append(event_record)
        
        # Maintain history size limit
        if len(self.event_history) > self.max_history_size:
            self.event_history = self.event_history[-self.max_history_size:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get dispatcher statistics."""
        event_type_counts = {}
        for event in self.event_history:
            event_type = event["event_type"]
            event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1
        
        return {
            "total_events_dispatched": len(self.event_history),
            "registered_handler_types": len(self.handlers),
            "total_handlers": sum(len(handlers) for handlers in self.handlers.values()),
            "event_type_counts": event_type_counts,
            "most_recent_event": self.event_history[-1] if self.event_history else None
        }


# Global event dispatcher instance
_global_dispatcher: Optional[EventDispatcher] = None


def get_event_dispatcher() -> EventDispatcher:
    """Get the global event dispatcher instance."""
    global _global_dispatcher
    if _global_dispatcher is None:
        _global_dispatcher = EventDispatcher()
    return _global_dispatcher


def set_event_dispatcher(dispatcher: EventDispatcher) -> None:
    """Set the global event dispatcher instance."""
    global _global_dispatcher
    _global_dispatcher = dispatcher
