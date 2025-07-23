"""
API v1 router configuration.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import opportunities, attachments

# Create API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    opportunities.router,
    prefix="/opportunities",
    tags=["opportunities"]
)

api_router.include_router(
    attachments.router,
    prefix="",  # No prefix as attachments have mixed paths
    tags=["attachments"]
)
