"""
Custom exceptions and exception handling utilities.
"""

from typing import List, Dict, Any
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import uuid


class ValidationException(Exception):
    """Custom validation exception."""
    def __init__(self, message: str, details: List[Dict[str, str]] = None):
        self.message = message
        self.details = details or []
        super().__init__(self.message)


class NotFoundException(Exception):
    """Custom not found exception."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class OperationNotAllowedException(Exception):
    """Custom operation not allowed exception."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def create_error_response(
    request: Request,
    error_code: str,
    message: str,
    details: List[Dict[str, str]] = None,
    status_code: int = 400
) -> JSONResponse:
    """Create standardized error response."""
    request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": error_code,
                "message": message,
                "details": details or []
            },
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "request_id": request_id
            }
        }
    )


async def validation_exception_handler(request: Request, exc: ValidationException):
    """Handle validation exceptions."""
    return create_error_response(
        request=request,
        error_code="VALIDATION_ERROR",
        message=exc.message,
        details=exc.details,
        status_code=400
    )


async def not_found_exception_handler(request: Request, exc: NotFoundException):
    """Handle not found exceptions."""
    return create_error_response(
        request=request,
        error_code="RESOURCE_NOT_FOUND",
        message=exc.message,
        status_code=404
    )


async def operation_not_allowed_exception_handler(request: Request, exc: OperationNotAllowedException):
    """Handle operation not allowed exceptions."""
    return create_error_response(
        request=request,
        error_code="OPERATION_NOT_ALLOWED",
        message=exc.message,
        status_code=403
    )
