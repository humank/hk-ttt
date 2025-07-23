"""
Common utilities and base classes for the Opportunity Management Service.
"""

import uuid
import datetime
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, TypeVar, Generic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Type variable for generic repository
T = TypeVar('T')

# Simple event system
class EventPublisher:
    """Simple event publisher for domain events."""
    
    _subscribers = {}
    
    @classmethod
    def subscribe(cls, event_type: str, callback):
        """Subscribe to an event type."""
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        cls._subscribers[event_type].append(callback)
        logger.info(f"Subscribed to event: {event_type}")
    
    @classmethod
    def publish(cls, event_type: str, data: Any):
        """Publish an event."""
        logger.info(f"Publishing event: {event_type}")
        if event_type in cls._subscribers:
            for callback in cls._subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Error in event subscriber: {e}")

# Base repository interface
class Repository(Generic[T], ABC):
    """Base repository interface for all entities."""
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Add an entity to the repository."""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: uuid.UUID) -> Optional[T]:
        """Get an entity by its ID."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an entity in the repository."""
        pass
    
    @abstractmethod
    def remove(self, entity_id: uuid.UUID) -> bool:
        """Remove an entity from the repository."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities from the repository."""
        pass

# Custom exceptions
class DomainException(Exception):
    """Base exception for all domain exceptions."""
    pass

class ValidationException(DomainException):
    """Exception raised for validation errors."""
    pass

class NotFoundException(DomainException):
    """Exception raised when an entity is not found."""
    pass

class OperationNotAllowedException(DomainException):
    """Exception raised when an operation is not allowed."""
    pass
