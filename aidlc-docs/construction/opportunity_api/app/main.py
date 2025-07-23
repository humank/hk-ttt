"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import uuid
import os
from datetime import datetime

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import engine, Base
from app.core.exceptions import (
    ValidationException, NotFoundException, OperationNotAllowedException,
    validation_exception_handler, not_found_exception_handler, 
    operation_not_allowed_exception_handler
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title="Opportunity Management Service API",
    description="RESTful API for managing opportunities, problem statements, skill requirements, timeline requirements, and attachments",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add custom exception handlers
app.add_exception_handler(ValidationException, validation_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(OperationNotAllowedException, operation_not_allowed_exception_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response middleware
@app.middleware("http")
async def add_request_id_middleware(request: Request, call_next):
    """Add request ID and logging middleware."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Log request
    logger.info(
        f"Request {request_id}: {request.method} {request.url.path} "
        f"from {request.client.host if request.client else 'unknown'}"
    )
    
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    
    # Add request ID to response headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log response
    logger.info(
        f"Response {request_id}: {response.status_code} "
        f"processed in {process_time:.3f}s"
    )
    
    return response

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Mount static files for web interface
web_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web")
if os.path.exists(web_dir):
    app.mount("/static", StaticFiles(directory=web_dir), name="static")
    logger.info(f"Mounted static files from: {web_dir}")

# Web interface route
@app.get("/web")
async def web_interface():
    """Serve the web interface."""
    web_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web", "index.html")
    if os.path.exists(web_file):
        return FileResponse(web_file)
    else:
        return {"message": "Web interface not found", "path": web_file}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Opportunity Management Service API",
        "version": "1.0.0",
        "documentation": "/api/v1/docs",
        "web_interface": "/web",
        "health": "/health",
        "openapi": "/api/v1/openapi.json"
    }

# Health check endpoint
@app.get("/health")
@limiter.limit("10/minute")
async def health_check(request: Request):
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))
    
    logger.error(f"Unhandled exception {request_id}: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal server error occurred",
                "details": []
            },
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "request_id": request_id
            }
        }
    )

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
