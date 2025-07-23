# Step 6: Implement API Layer

This document outlines the implementation of the API layer for the Opportunity Management Service.

## API Definitions

### RESTful Endpoints

Based on our domain model and service layer, we'll expose the following RESTful endpoints:

#### Opportunity Endpoints

1. **Create Opportunity**
   - **Method**: POST
   - **Path**: `/api/v1/opportunities`
   - **Request Body**: OpportunityCreateRequest
   - **Response**: OpportunityResponse
   - **Status Codes**: 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden

2. **Get Opportunity**
   - **Method**: GET
   - **Path**: `/api/v1/opportunities/{opportunityId}`
   - **Parameters**: opportunityId (path)
   - **Response**: OpportunityResponse
   - **Status Codes**: 200 OK, 404 Not Found, 401 Unauthorized, 403 Forbidden

3. **Update Opportunity**
   - **Method**: PUT
   - **Path**: `/api/v1/opportunities/{opportunityId}`
   - **Parameters**: opportunityId (path)
   - **Request Body**: OpportunityUpdateRequest
   - **Response**: OpportunityResponse
   - **Status Codes**: 200 OK, 400 Bad Request, 404 Not Found, 401 Unauthorized, 403 Forbidden

4. **Delete Opportunity**
   - **Method**: DELETE
   - **Path**: `/api/v1/opportunities/{opportunityId}`
   - **Parameters**: opportunityId (path)
   - **Response**: No content
   - **Status Codes**: 204 No Content, 404 Not Found, 401 Unauthorized, 403 Forbidden

5. **List Opportunities**
   - **Method**: GET
   - **Path**: `/api/v1/opportunities`
   - **Query Parameters**: 
     - page (integer, default: 0)
     - size (integer, default: 20)
     - status (string, optional)
     - sortBy (string, optional)
     - sortDirection (string, optional)
   - **Response**: PagedOpportunityResponse
   - **Status Codes**: 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden

6. **Change Opportunity Status**
   - **Method**: POST
   - **Path**: `/api/v1/opportunities/{opportunityId}/status`
   - **Parameters**: opportunityId (path)
   - **Request Body**: StatusChangeRequest
   - **Response**: OpportunityResponse
   - **Status Codes**: 200 OK, 400 Bad Request, 404 Not Found, 401 Unauthorized, 403 Forbidden

#### Problem Statement Endpoints

1. **Add Problem Statement**
   - **Method**: POST
   - **Path**: `/api/v1/opportunities/{opportunityId}/problem-statements`
   - **Parameters**: opportunityId (path)
   - **Request Body**: ProblemStatementRequest
   - **Response**: ProblemStatementResponse
   - **Status Codes**: 201 Created, 400 Bad Request, 404 Not Found, 401 Unauthorized, 403 Forbidden

2. **Update Problem Statement**
   - **Method**: PUT
   - **Path**: `/api/v1/opportunities/{opportunityId}/problem-statements/{statementId}`
   - **Parameters**: opportunityId (path), statementId (path)
   - **Request Body**: ProblemStatementRequest
   - **Response**: ProblemStatementResponse
   - **Status Codes**: 200 OK, 400 Bad Request, 404 Not Found, 401 Unauthorized, 403 Forbidden

3. **Delete Problem Statement**
   - **Method**: DELETE
   - **Path**: `/api/v1/opportunities/{opportunityId}/problem-statements/{statementId}`
   - **Parameters**: opportunityId (path), statementId (path)
   - **Response**: No content
   - **Status Codes**: 204 No Content, 404 Not Found, 401 Unauthorized, 403 Forbidden

#### Skill Requirement Endpoints

1. **Add Skill Requirement**
   - **Method**: POST
   - **Path**: `/api/v1/opportunities/{opportunityId}/skill-requirements`
   - **Parameters**: opportunityId (path)
   - **Request Body**: SkillRequirementRequest
   - **Response**: SkillRequirementResponse
   - **Status Codes**: 201 Created, 400 Bad Request, 404 Not Found, 401 Unauthorized, 403 Forbidden

2. **Update Skill Requirement**
   - **Method**: PUT
   - **Path**: `/api/v1/opportunities/{opportunityId}/skill-requirements/{requirementId}`
   - **Parameters**: opportunityId (path), requirementId (path)
   - **Request Body**: SkillRequirementRequest
   - **Response**: SkillRequirementResponse
   - **Status Codes**: 200 OK, 400 Bad Request, 404 Not Found, 401 Unauthorized, 403 Forbidden

3. **Delete Skill Requirement**
   - **Method**: DELETE
   - **Path**: `/api/v1/opportunities/{opportunityId}/skill-requirements/{requirementId}`
   - **Parameters**: opportunityId (path), requirementId (path)
   - **Response**: No content
   - **Status Codes**: 204 No Content, 404 Not Found, 401 Unauthorized, 403 Forbidden

#### Timeline Requirement Endpoints

1. **Add Timeline Requirement**
   - **Method**: POST
   - **Path**: `/api/v1/opportunities/{opportunityId}/timeline-requirements`
   - **Parameters**: opportunityId (path)
   - **Request Body**: TimelineRequirementRequest
   - **Response**: TimelineRequirementResponse
   - **Status Codes**: 201 Created, 400 Bad Request, 404 Not Found, 401 Unauthorized, 403 Forbidden

2. **Update Timeline Requirement**
   - **Method**: PUT
   - **Path**: `/api/v1/opportunities/{opportunityId}/timeline-requirements/{requirementId}`
   - **Parameters**: opportunityId (path), requirementId (path)
   - **Request Body**: TimelineRequirementRequest
   - **Response**: TimelineRequirementResponse
   - **Status Codes**: 200 OK, 400 Bad Request, 404 Not Found, 401 Unauthorized, 403 Forbidden

3. **Delete Timeline Requirement**
   - **Method**: DELETE
   - **Path**: `/api/v1/opportunities/{opportunityId}/timeline-requirements/{requirementId}`
   - **Parameters**: opportunityId (path), requirementId (path)
   - **Response**: No content
   - **Status Codes**: 204 No Content, 404 Not Found, 401 Unauthorized, 403 Forbidden

#### Attachment Endpoints

1. **Get Upload URL**
   - **Method**: POST
   - **Path**: `/api/v1/opportunities/{opportunityId}/attachments/upload-url`
   - **Parameters**: opportunityId (path)
   - **Request Body**: UploadUrlRequest
   - **Response**: UploadUrlResponse
   - **Status Codes**: 200 OK, 400 Bad Request, 404 Not Found, 401 Unauthorized, 403 Forbidden

2. **Complete Upload**
   - **Method**: POST
   - **Path**: `/api/v1/opportunities/{opportunityId}/attachments/complete`
   - **Parameters**: opportunityId (path)
   - **Request Body**: CompleteUploadRequest
   - **Response**: AttachmentResponse
   - **Status Codes**: 201 Created, 400 Bad Request, 404 Not Found, 401 Unauthorized, 403 Forbidden

3. **Delete Attachment**
   - **Method**: DELETE
   - **Path**: `/api/v1/opportunities/{opportunityId}/attachments/{attachmentId}`
   - **Parameters**: opportunityId (path), attachmentId (path)
   - **Response**: No content
   - **Status Codes**: 204 No Content, 404 Not Found, 401 Unauthorized, 403 Forbidden

4. **Get Download URL**
   - **Method**: GET
   - **Path**: `/api/v1/opportunities/{opportunityId}/attachments/{attachmentId}/download-url`
   - **Parameters**: opportunityId (path), attachmentId (path)
   - **Response**: DownloadUrlResponse
   - **Status Codes**: 200 OK, 404 Not Found, 401 Unauthorized, 403 Forbidden

### Request/Response Models

#### Opportunity Models

```python
class OpportunityCreateRequest:
    title: str
    description: str
    client_name: str
    estimated_budget: float
    estimated_start_date: datetime
    estimated_end_date: datetime
    status: str = "DRAFT"  # Default value

class OpportunityUpdateRequest:
    title: str = None
    description: str = None
    client_name: str = None
    estimated_budget: float = None
    estimated_start_date: datetime = None
    estimated_end_date: datetime = None

class OpportunityResponse:
    id: str
    title: str
    description: str
    client_name: str
    estimated_budget: float
    estimated_start_date: datetime
    estimated_end_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    created_by: str
    problem_statements: List[ProblemStatementResponse]
    skill_requirements: List[SkillRequirementResponse]
    timeline_requirements: List[TimelineRequirementResponse]
    attachments: List[AttachmentResponse]
    change_history: List[ChangeRecordResponse]

class PagedOpportunityResponse:
    items: List[OpportunityResponse]
    total_items: int
    page: int
    size: int
    total_pages: int

class StatusChangeRequest:
    new_status: str
    reason: str
```

#### Problem Statement Models

```python
class ProblemStatementRequest:
    description: str
    priority: int = 1  # Default value

class ProblemStatementResponse:
    id: str
    description: str
    priority: int
    created_at: datetime
    updated_at: datetime
```

#### Skill Requirement Models

```python
class SkillRequirementRequest:
    skill_name: str
    experience_level: str
    importance: str = "MEDIUM"  # Default value

class SkillRequirementResponse:
    id: str
    skill_name: str
    experience_level: str
    importance: str
    created_at: datetime
    updated_at: datetime
```

#### Timeline Requirement Models

```python
class TimelineRequirementRequest:
    description: str
    target_date: datetime
    type: str = "MILESTONE"  # Default value

class TimelineRequirementResponse:
    id: str
    description: str
    target_date: datetime
    type: str
    created_at: datetime
    updated_at: datetime
```

#### Attachment Models

```python
class UploadUrlRequest:
    file_name: str
    content_type: str
    file_size: int

class UploadUrlResponse:
    upload_url: str
    key: str
    expires_at: datetime

class CompleteUploadRequest:
    key: str
    file_name: str
    content_type: str
    file_size: int
    description: str = None

class AttachmentResponse:
    id: str
    file_name: str
    content_type: str
    file_size: int
    description: str
    created_at: datetime
    created_by: str
```

#### Change Record Models

```python
class ChangeRecordResponse:
    id: str
    field_name: str
    old_value: str
    new_value: str
    changed_at: datetime
    changed_by: str
```

## Request/Response Serialization

We'll use Python's FastAPI framework for automatic request/response serialization. FastAPI uses Pydantic models for validation and serialization, which aligns well with our domain model.

### Serialization Example

```python
from fastapi import FastAPI, HTTPException, Depends, Path, Query
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Pydantic models for request/response serialization
class OpportunityCreateRequest(BaseModel):
    title: str
    description: str
    client_name: str
    estimated_budget: float
    estimated_start_date: datetime
    estimated_end_date: datetime
    status: str = "DRAFT"

# FastAPI route example
@app.post("/api/v1/opportunities", response_model=OpportunityResponse, status_code=201)
async def create_opportunity(
    request: OpportunityCreateRequest,
    current_user: User = Depends(get_current_user)
):
    # Convert request to domain model
    opportunity = Opportunity(
        id=str(uuid.uuid4()),
        title=request.title,
        description=request.description,
        client_name=request.client_name,
        estimated_budget=request.estimated_budget,
        estimated_start_date=request.estimated_start_date,
        estimated_end_date=request.estimated_end_date,
        status=OpportunityStatus(request.status),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        created_by=current_user.id
    )
    
    # Call service layer
    try:
        created_opportunity = opportunity_service.create_opportunity(opportunity, current_user)
        # Convert domain model to response
        return map_to_opportunity_response(created_opportunity)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AuthorizationError as e:
        raise HTTPException(status_code=403, detail=str(e))
```

## Error Handling

We'll implement a consistent error handling approach across the API:

### Error Response Format

```python
class ErrorResponse(BaseModel):
    status_code: int
    message: str
    details: Optional[List[ErrorDetail]] = None
    request_id: str

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str
    code: str
```

### Error Handling Middleware

```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_response = ErrorResponse(
        status_code=exc.status_code,
        message=exc.detail,
        request_id=request.headers.get("X-Request-ID", str(uuid.uuid4()))
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    details = [
        ErrorDetail(
            field=e["loc"][-1] if e["loc"] else None,
            message=e["msg"],
            code=e["type"]
        )
        for e in exc.errors()
    ]
    error_response = ErrorResponse(
        status_code=400,
        message="Validation error",
        details=details,
        request_id=request.headers.get("X-Request-ID", str(uuid.uuid4()))
    )
    return JSONResponse(
        status_code=400,
        content=error_response.dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Log the exception
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    error_response = ErrorResponse(
        status_code=500,
        message="Internal server error",
        request_id=request.headers.get("X-Request-ID", str(uuid.uuid4()))
    )
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )
```

## Authentication and Authorization Implementation

### JWT Token Validation

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode JWT token
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # Get user from cache or database
        user = await get_user_from_cache_or_db(user_id)
        if user is None:
            raise credentials_exception
            
        return user
    except JWTError:
        raise credentials_exception
```

### Role-Based Access Control

```python
from fastapi import Depends, HTTPException, status
from enum import Enum

class Role(str, Enum):
    ADMIN = "ADMIN"
    SALES_MANAGER = "SALES_MANAGER"
    SALES_REPRESENTATIVE = "SALES_REPRESENTATIVE"

def has_role(required_roles: List[Role]):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have required role. Required: {required_roles}, actual: {current_user.role}"
            )
        return current_user
    return role_checker

# Usage in route
@app.post("/api/v1/opportunities", response_model=OpportunityResponse)
async def create_opportunity(
    request: OpportunityCreateRequest,
    current_user: User = Depends(has_role([Role.ADMIN, Role.SALES_MANAGER]))
):
    # Implementation
    pass
```

### Resource-Based Authorization

```python
async def can_access_opportunity(
    opportunity_id: str,
    current_user: User = Depends(get_current_user)
):
    # Check if user has access to the opportunity
    opportunity = await opportunity_service.get_opportunity(opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    
    # Admins can access all opportunities
    if current_user.role == Role.ADMIN:
        return opportunity
    
    # Sales managers can access all opportunities
    if current_user.role == Role.SALES_MANAGER:
        return opportunity
    
    # Sales representatives can only access their own opportunities
    if current_user.role == Role.SALES_REPRESENTATIVE and opportunity.created_by == current_user.id:
        return opportunity
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You don't have permission to access this opportunity"
    )

# Usage in route
@app.get("/api/v1/opportunities/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(
    opportunity: Opportunity = Depends(can_access_opportunity)
):
    return map_to_opportunity_response(opportunity)
```

## API Documentation

We'll use FastAPI's built-in Swagger UI and ReDoc for API documentation:

```python
from fastapi import FastAPI

app = FastAPI(
    title="Opportunity Management Service API",
    description="API for managing sales opportunities",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)
```

## API Versioning Strategy

We'll use URL path versioning for our API:

1. **Current Version**: `/api/v1/...`
2. **Future Versions**: `/api/v2/...`, `/api/v3/...`, etc.

When introducing breaking changes, we'll:
1. Create a new API version
2. Support the old version for a deprecation period (minimum 6 months)
3. Provide migration documentation for clients

## Rate Limiting

We'll implement rate limiting at the API Gateway level:

1. **Default Limits**:
   - Authenticated users: 100 requests per minute
   - Unauthenticated users: 10 requests per minute

2. **Endpoint-Specific Limits**:
   - List operations: 50 requests per minute
   - Create/Update operations: 30 requests per minute

3. **Response Headers**:
   - `X-RateLimit-Limit`: Maximum requests per minute
   - `X-RateLimit-Remaining`: Remaining requests in the current window
   - `X-RateLimit-Reset`: Time when the rate limit resets (Unix timestamp)

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app.example.com",
        "https://admin.example.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    max_age=86400  # 24 hours
)
```

## Health Check Endpoints

```python
from fastapi import FastAPI, Depends, Response, status

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

@app.get("/health/detailed", tags=["Health"])
async def detailed_health_check():
    # Check database connection
    db_status = await check_database_connection()
    
    # Check cache connection
    cache_status = await check_cache_connection()
    
    # Check S3 connection
    s3_status = await check_s3_connection()
    
    # Overall status
    overall_status = "healthy" if all([
        db_status["status"] == "healthy",
        cache_status["status"] == "healthy",
        s3_status["status"] == "healthy"
    ]) else "unhealthy"
    
    return {
        "status": overall_status,
        "components": {
            "database": db_status,
            "cache": cache_status,
            "storage": s3_status
        },
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }
```

## API Metrics and Logging

We'll implement comprehensive API metrics and logging:

### Request Logging Middleware

```python
import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start_time = time.time()
        
        # Add request_id to request state
        request.state.request_id = request_id
        
        # Log request
        logger.info(f"Request started", extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host
        })
        
        try:
            response = await call_next(request)
            
            # Log response
            process_time = time.time() - start_time
            logger.info(f"Request completed", extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time_ms": round(process_time * 1000, 2)
            })
            
            # Add headers to response
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))
            
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"Request failed", extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "error": str(e),
                "process_time_ms": round(process_time * 1000, 2)
            })
            raise

app.add_middleware(RequestLoggingMiddleware)
```

### Custom Metrics

```python
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import FastAPI, Response

# Define metrics
REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total count of API requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "api_request_duration_seconds",
    "API request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
)

# Middleware to record metrics
class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        # Record metrics
        duration = time.time() - start_time
        endpoint = request.url.path
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status_code=response.status_code
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)
        
        return response

app.add_middleware(MetricsMiddleware)

# Metrics endpoint
@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
```

## Next Steps

1. Implement the API layer using FastAPI
2. Create request/response models
3. Implement error handling middleware
4. Implement authentication and authorization
5. Set up API documentation
6. Implement health check endpoints
7. Set up metrics and logging
