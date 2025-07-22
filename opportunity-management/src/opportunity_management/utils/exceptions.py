"""
Custom domain exceptions for the opportunity management system.
"""

from typing import List, Optional, Dict, Any


class DomainException(Exception):
    """Base exception for all domain-related errors."""
    
    def __init__(self, message: str, error_code: Optional[str] = None, 
                 details: Optional[Dict[str, Any]] = None):
        """Initialize domain exception."""
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary representation."""
        return {
            "error_type": self.__class__.__name__,
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details
        }


class ValidationException(DomainException):
    """Exception raised when validation fails."""
    
    def __init__(self, message: str, validation_errors: List[str], 
                 field: Optional[str] = None):
        """Initialize validation exception."""
        super().__init__(message, "VALIDATION_ERROR")
        self.validation_errors = validation_errors
        self.field = field
        self.details = {
            "validation_errors": validation_errors,
            "field": field
        }


class OpportunityNotFoundException(DomainException):
    """Exception raised when opportunity is not found."""
    
    def __init__(self, opportunity_id: str):
        """Initialize opportunity not found exception."""
        message = f"Opportunity with ID '{opportunity_id}' not found"
        super().__init__(message, "OPPORTUNITY_NOT_FOUND")
        self.opportunity_id = opportunity_id
        self.details = {"opportunity_id": opportunity_id}


class CustomerNotFoundException(DomainException):
    """Exception raised when customer is not found."""
    
    def __init__(self, customer_id: str):
        """Initialize customer not found exception."""
        message = f"Customer with ID '{customer_id}' not found"
        super().__init__(message, "CUSTOMER_NOT_FOUND")
        self.customer_id = customer_id
        self.details = {"customer_id": customer_id}


class InvalidStatusTransitionException(DomainException):
    """Exception raised when an invalid status transition is attempted."""
    
    def __init__(self, from_status: str, to_status: str, opportunity_id: str):
        """Initialize invalid status transition exception."""
        message = f"Cannot transition from '{from_status}' to '{to_status}' for opportunity '{opportunity_id}'"
        super().__init__(message, "INVALID_STATUS_TRANSITION")
        self.from_status = from_status
        self.to_status = to_status
        self.opportunity_id = opportunity_id
        self.details = {
            "from_status": from_status,
            "to_status": to_status,
            "opportunity_id": opportunity_id
        }


class OpportunityNotModifiableException(DomainException):
    """Exception raised when trying to modify a non-modifiable opportunity."""
    
    def __init__(self, opportunity_id: str, current_status: str):
        """Initialize opportunity not modifiable exception."""
        message = f"Opportunity '{opportunity_id}' cannot be modified in '{current_status}' status"
        super().__init__(message, "OPPORTUNITY_NOT_MODIFIABLE")
        self.opportunity_id = opportunity_id
        self.current_status = current_status
        self.details = {
            "opportunity_id": opportunity_id,
            "current_status": current_status
        }


class DuplicateSkillRequirementException(DomainException):
    """Exception raised when trying to add duplicate skill requirement."""
    
    def __init__(self, skill_name: str, skill_category: str):
        """Initialize duplicate skill requirement exception."""
        message = f"Skill requirement '{skill_name}' in category '{skill_category}' already exists"
        super().__init__(message, "DUPLICATE_SKILL_REQUIREMENT")
        self.skill_name = skill_name
        self.skill_category = skill_category
        self.details = {
            "skill_name": skill_name,
            "skill_category": skill_category
        }


class TimelineValidationException(DomainException):
    """Exception raised when timeline validation fails."""
    
    def __init__(self, message: str, timeline_errors: List[str]):
        """Initialize timeline validation exception."""
        super().__init__(message, "TIMELINE_VALIDATION_ERROR")
        self.timeline_errors = timeline_errors
        self.details = {"timeline_errors": timeline_errors}


class BusinessRuleViolationException(DomainException):
    """Exception raised when business rules are violated."""
    
    def __init__(self, rule_name: str, message: str, context: Optional[Dict[str, Any]] = None):
        """Initialize business rule violation exception."""
        super().__init__(message, "BUSINESS_RULE_VIOLATION")
        self.rule_name = rule_name
        self.context = context or {}
        self.details = {
            "rule_name": rule_name,
            "context": self.context
        }


class ReactivationNotAllowedException(DomainException):
    """Exception raised when opportunity reactivation is not allowed."""
    
    def __init__(self, opportunity_id: str, reason: str):
        """Initialize reactivation not allowed exception."""
        message = f"Opportunity '{opportunity_id}' cannot be reactivated: {reason}"
        super().__init__(message, "REACTIVATION_NOT_ALLOWED")
        self.opportunity_id = opportunity_id
        self.reason = reason
        self.details = {
            "opportunity_id": opportunity_id,
            "reason": reason
        }


class ArchitectSelectionException(DomainException):
    """Exception raised when architect selection fails."""
    
    def __init__(self, opportunity_id: str, architect_id: str, reason: str):
        """Initialize architect selection exception."""
        message = f"Cannot select architect '{architect_id}' for opportunity '{opportunity_id}': {reason}"
        super().__init__(message, "ARCHITECT_SELECTION_ERROR")
        self.opportunity_id = opportunity_id
        self.architect_id = architect_id
        self.reason = reason
        self.details = {
            "opportunity_id": opportunity_id,
            "architect_id": architect_id,
            "reason": reason
        }


class DocumentAttachmentException(DomainException):
    """Exception raised when document attachment operations fail."""
    
    def __init__(self, message: str, file_name: Optional[str] = None, 
                 file_size: Optional[int] = None):
        """Initialize document attachment exception."""
        super().__init__(message, "DOCUMENT_ATTACHMENT_ERROR")
        self.file_name = file_name
        self.file_size = file_size
        self.details = {
            "file_name": file_name,
            "file_size": file_size
        }


class RepositoryException(DomainException):
    """Exception raised when repository operations fail."""
    
    def __init__(self, message: str, operation: str, entity_type: str, 
                 entity_id: Optional[str] = None):
        """Initialize repository exception."""
        super().__init__(message, "REPOSITORY_ERROR")
        self.operation = operation
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.details = {
            "operation": operation,
            "entity_type": entity_type,
            "entity_id": entity_id
        }


class ConcurrencyException(DomainException):
    """Exception raised when concurrency conflicts occur."""
    
    def __init__(self, entity_id: str, entity_type: str, expected_version: int, 
                 actual_version: int):
        """Initialize concurrency exception."""
        message = f"Concurrency conflict for {entity_type} '{entity_id}': expected version {expected_version}, actual version {actual_version}"
        super().__init__(message, "CONCURRENCY_CONFLICT")
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.expected_version = expected_version
        self.actual_version = actual_version
        self.details = {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "expected_version": expected_version,
            "actual_version": actual_version
        }


# Exception handler utility functions

def handle_validation_errors(errors: List[str], field: Optional[str] = None) -> None:
    """Raise ValidationException if errors exist."""
    if errors:
        message = f"Validation failed: {'; '.join(errors)}"
        raise ValidationException(message, errors, field)


def handle_business_rule_violation(rule_name: str, message: str, 
                                 context: Optional[Dict[str, Any]] = None) -> None:
    """Raise BusinessRuleViolationException."""
    raise BusinessRuleViolationException(rule_name, message, context)


def wrap_repository_exception(operation: str, entity_type: str, 
                            entity_id: Optional[str] = None) -> callable:
    """Decorator to wrap repository exceptions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if isinstance(e, DomainException):
                    raise
                message = f"Repository operation '{operation}' failed for {entity_type}: {str(e)}"
                raise RepositoryException(message, operation, entity_type, entity_id)
        return wrapper
    return decorator
