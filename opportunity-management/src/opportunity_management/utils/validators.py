"""
Common validation utilities for the opportunity management system.
"""

import re
from typing import List, Optional, Any, Dict
from datetime import date, datetime
from decimal import Decimal, InvalidOperation


class ValidationResult:
    """Result of a validation operation."""
    
    def __init__(self, is_valid: bool = True, errors: Optional[List[str]] = None):
        """Initialize validation result."""
        self.is_valid = is_valid
        self.errors = errors or []
    
    def add_error(self, error: str) -> None:
        """Add an error to the validation result."""
        self.errors.append(error)
        self.is_valid = False
    
    def merge(self, other: 'ValidationResult') -> 'ValidationResult':
        """Merge with another validation result."""
        combined_errors = self.errors + other.errors
        return ValidationResult(
            is_valid=self.is_valid and other.is_valid,
            errors=combined_errors
        )


class StringValidator:
    """Validator for string fields."""
    
    @staticmethod
    def is_not_empty(value: str, field_name: str = "Field") -> ValidationResult:
        """Validate that string is not empty."""
        if not value or not value.strip():
            return ValidationResult(False, [f"{field_name} cannot be empty"])
        return ValidationResult()
    
    @staticmethod
    def min_length(value: str, min_len: int, field_name: str = "Field") -> ValidationResult:
        """Validate minimum string length."""
        if len(value.strip()) < min_len:
            return ValidationResult(False, [f"{field_name} must be at least {min_len} characters"])
        return ValidationResult()
    
    @staticmethod
    def max_length(value: str, max_len: int, field_name: str = "Field") -> ValidationResult:
        """Validate maximum string length."""
        if len(value) > max_len:
            return ValidationResult(False, [f"{field_name} cannot exceed {max_len} characters"])
        return ValidationResult()
    
    @staticmethod
    def matches_pattern(value: str, pattern: str, field_name: str = "Field", 
                       error_message: Optional[str] = None) -> ValidationResult:
        """Validate string matches regex pattern."""
        if not re.match(pattern, value):
            message = error_message or f"{field_name} format is invalid"
            return ValidationResult(False, [message])
        return ValidationResult()
    
    @staticmethod
    def is_valid_email(email: str) -> ValidationResult:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return StringValidator.matches_pattern(
            email, pattern, "Email", "Invalid email format"
        )
    
    @staticmethod
    def is_in_choices(value: str, choices: List[str], field_name: str = "Field") -> ValidationResult:
        """Validate string is in allowed choices."""
        if value not in choices:
            return ValidationResult(False, [f"{field_name} must be one of: {', '.join(choices)}"])
        return ValidationResult()


class NumericValidator:
    """Validator for numeric fields."""
    
    @staticmethod
    def is_positive(value: float, field_name: str = "Field") -> ValidationResult:
        """Validate number is positive."""
        if value <= 0:
            return ValidationResult(False, [f"{field_name} must be positive"])
        return ValidationResult()
    
    @staticmethod
    def is_non_negative(value: float, field_name: str = "Field") -> ValidationResult:
        """Validate number is non-negative."""
        if value < 0:
            return ValidationResult(False, [f"{field_name} cannot be negative"])
        return ValidationResult()
    
    @staticmethod
    def is_in_range(value: float, min_val: float, max_val: float, 
                   field_name: str = "Field") -> ValidationResult:
        """Validate number is within range."""
        if not (min_val <= value <= max_val):
            return ValidationResult(False, [f"{field_name} must be between {min_val} and {max_val}"])
        return ValidationResult()
    
    @staticmethod
    def is_valid_decimal(value: str, field_name: str = "Field") -> ValidationResult:
        """Validate string can be converted to decimal."""
        try:
            Decimal(value)
            return ValidationResult()
        except (InvalidOperation, ValueError):
            return ValidationResult(False, [f"{field_name} must be a valid decimal number"])
    
    @staticmethod
    def is_valid_percentage(value: int, field_name: str = "Field") -> ValidationResult:
        """Validate percentage (0-100)."""
        return NumericValidator.is_in_range(value, 0, 100, field_name)


class DateValidator:
    """Validator for date fields."""
    
    @staticmethod
    def is_not_in_past(value: date, field_name: str = "Date") -> ValidationResult:
        """Validate date is not in the past."""
        if value < date.today():
            return ValidationResult(False, [f"{field_name} cannot be in the past"])
        return ValidationResult()
    
    @staticmethod
    def is_after(value: date, after_date: date, field_name: str = "Date") -> ValidationResult:
        """Validate date is after another date."""
        if value <= after_date:
            return ValidationResult(False, [f"{field_name} must be after {after_date}"])
        return ValidationResult()
    
    @staticmethod
    def is_within_range(value: date, start_date: date, end_date: date, 
                       field_name: str = "Date") -> ValidationResult:
        """Validate date is within range."""
        if not (start_date <= value <= end_date):
            return ValidationResult(False, [f"{field_name} must be between {start_date} and {end_date}"])
        return ValidationResult()
    
    @staticmethod
    def is_valid_date_string(value: str, field_name: str = "Date") -> ValidationResult:
        """Validate string can be parsed as date."""
        try:
            date.fromisoformat(value)
            return ValidationResult()
        except ValueError:
            return ValidationResult(False, [f"{field_name} must be in YYYY-MM-DD format"])
    
    @staticmethod
    def is_business_day(value: date, field_name: str = "Date") -> ValidationResult:
        """Validate date is a business day (Monday-Friday)."""
        if value.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return ValidationResult(False, [f"{field_name} must be a business day"])
        return ValidationResult()


class CollectionValidator:
    """Validator for collections (lists, sets, etc.)."""
    
    @staticmethod
    def is_not_empty(collection: List[Any], field_name: str = "Collection") -> ValidationResult:
        """Validate collection is not empty."""
        if not collection:
            return ValidationResult(False, [f"{field_name} cannot be empty"])
        return ValidationResult()
    
    @staticmethod
    def min_length(collection: List[Any], min_len: int, 
                  field_name: str = "Collection") -> ValidationResult:
        """Validate minimum collection length."""
        if len(collection) < min_len:
            return ValidationResult(False, [f"{field_name} must have at least {min_len} items"])
        return ValidationResult()
    
    @staticmethod
    def max_length(collection: List[Any], max_len: int, 
                  field_name: str = "Collection") -> ValidationResult:
        """Validate maximum collection length."""
        if len(collection) > max_len:
            return ValidationResult(False, [f"{field_name} cannot have more than {max_len} items"])
        return ValidationResult()
    
    @staticmethod
    def has_no_duplicates(collection: List[Any], field_name: str = "Collection") -> ValidationResult:
        """Validate collection has no duplicates."""
        if len(collection) != len(set(collection)):
            return ValidationResult(False, [f"{field_name} cannot contain duplicates"])
        return ValidationResult()
    
    @staticmethod
    def all_items_valid(collection: List[Any], item_validator: callable, 
                       field_name: str = "Collection") -> ValidationResult:
        """Validate all items in collection pass validation."""
        result = ValidationResult()
        for i, item in enumerate(collection):
            item_result = item_validator(item)
            if not item_result.is_valid:
                for error in item_result.errors:
                    result.add_error(f"{field_name}[{i}]: {error}")
        return result


class FileValidator:
    """Validator for file-related fields."""
    
    @staticmethod
    def is_valid_file_size(size_bytes: int, max_size_mb: int = 20) -> ValidationResult:
        """Validate file size is within limits."""
        max_size_bytes = max_size_mb * 1024 * 1024
        if size_bytes > max_size_bytes:
            return ValidationResult(False, [f"File size exceeds maximum limit of {max_size_mb}MB"])
        return ValidationResult()
    
    @staticmethod
    def is_valid_file_type(file_type: str, allowed_types: Optional[List[str]] = None) -> ValidationResult:
        """Validate file type is allowed."""
        if allowed_types and file_type.lower() not in [t.lower() for t in allowed_types]:
            return ValidationResult(False, [f"File type '{file_type}' is not allowed"])
        return ValidationResult()
    
    @staticmethod
    def is_valid_filename(filename: str) -> ValidationResult:
        """Validate filename format."""
        # Check for invalid characters
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
        if any(char in filename for char in invalid_chars):
            return ValidationResult(False, ["Filename contains invalid characters"])
        
        # Check length
        if len(filename) > 255:
            return ValidationResult(False, ["Filename is too long"])
        
        return ValidationResult()


class CompositeValidator:
    """Validator that combines multiple validation rules."""
    
    def __init__(self):
        """Initialize composite validator."""
        self.validators = []
    
    def add_validator(self, validator: callable) -> 'CompositeValidator':
        """Add a validator function."""
        self.validators.append(validator)
        return self
    
    def validate(self, value: Any) -> ValidationResult:
        """Run all validators and combine results."""
        result = ValidationResult()
        for validator in self.validators:
            validator_result = validator(value)
            result = result.merge(validator_result)
        return result


# Convenience functions for common validation patterns

def validate_required_string(value: str, field_name: str, 
                           min_length: Optional[int] = None,
                           max_length: Optional[int] = None) -> ValidationResult:
    """Validate required string field with optional length constraints."""
    result = StringValidator.is_not_empty(value, field_name)
    
    if result.is_valid and min_length:
        result = result.merge(StringValidator.min_length(value, min_length, field_name))
    
    if result.is_valid and max_length:
        result = result.merge(StringValidator.max_length(value, max_length, field_name))
    
    return result


def validate_positive_decimal(value: str, field_name: str) -> ValidationResult:
    """Validate positive decimal value."""
    result = NumericValidator.is_valid_decimal(value, field_name)
    
    if result.is_valid:
        decimal_value = float(Decimal(value))
        result = result.merge(NumericValidator.is_positive(decimal_value, field_name))
    
    return result


def validate_future_date(value: str, field_name: str) -> ValidationResult:
    """Validate date string is in future."""
    result = DateValidator.is_valid_date_string(value, field_name)
    
    if result.is_valid:
        date_value = date.fromisoformat(value)
        result = result.merge(DateValidator.is_not_in_past(date_value, field_name))
    
    return result


def validate_email_if_provided(email: Optional[str]) -> ValidationResult:
    """Validate email format if provided (optional field)."""
    if email and email.strip():
        return StringValidator.is_valid_email(email)
    return ValidationResult()


def validate_choice_field(value: str, choices: List[str], field_name: str) -> ValidationResult:
    """Validate required choice field."""
    result = StringValidator.is_not_empty(value, field_name)
    
    if result.is_valid:
        result = result.merge(StringValidator.is_in_choices(value, choices, field_name))
    
    return result
