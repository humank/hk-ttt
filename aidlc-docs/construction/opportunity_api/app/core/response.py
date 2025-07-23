"""
Response utilities for standardized API responses.
"""

from typing import Any, Dict, Optional
from fastapi import Request
from datetime import datetime
import uuid

from app.schemas.base import StandardResponse, ResponseMeta, PaginationInfo


def create_response(
    request: Request,
    data: Dict[str, Any],
    pagination: Optional[PaginationInfo] = None
) -> Dict[str, Any]:
    """Create standardized API response."""
    request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))
    
    response_data = {
        "data": data,
        "meta": {
            "timestamp": datetime.now().isoformat(),
            "request_id": request_id
        }
    }
    
    if pagination:
        response_data["pagination"] = pagination.dict()
    
    return response_data


def create_success_response(
    request: Request,
    data: Any,
    message: str = "Success"
) -> Dict[str, Any]:
    """Create success response with data."""
    return create_response(
        request=request,
        data={"result": data, "message": message}
    )


def create_list_response(
    request: Request,
    items: list,
    total_items: int,
    page: int = 1,
    page_size: int = 20
) -> Dict[str, Any]:
    """Create paginated list response."""
    total_pages = (total_items + page_size - 1) // page_size
    
    pagination = PaginationInfo(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages
    )
    
    return create_response(
        request=request,
        data={"items": items},
        pagination=pagination
    )
