# Troubleshooting Guide

## HTTP 404 Error - Root Cause and Solution

### Problem
You were getting a 404 error when accessing the root path `/` because the API didn't have a route defined for it.

### Root Cause
The original API only had routes under `/api/v1/` prefix, but no route for the root path `/`. When you tried to access `http://localhost:8000/`, the server couldn't find a matching route and returned a 404 error.

### Solution
Added a root endpoint that provides API information and navigation:

```python
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Opportunity Management Service API",
        "version": "1.0.0",
        "documentation": "/api/v1/docs",
        "health": "/health",
        "openapi": "/api/v1/openapi.json"
    }
```

## Other Issues Fixed

### 1. Pydantic BaseSettings Import Error
**Problem**: `BaseSettings` was moved to `pydantic-settings` package in Pydantic v2
**Solution**: 
- Installed `pydantic-settings` package
- Updated import: `from pydantic_settings import BaseSettings`

### 2. UUID Serialization Error
**Problem**: UUID objects in geographic_requirements couldn't be serialized to JSON
**Solution**: Convert UUID objects to strings before storing in database

### 3. SQLite Compatibility
**Problem**: PostgreSQL-specific UUID columns not compatible with SQLite
**Solution**: Changed all UUID columns to String(36) for SQLite compatibility

## Correct API Endpoints

### Available Endpoints:

1. **Root Information**
   ```bash
   GET http://localhost:8000/
   ```

2. **Health Check**
   ```bash
   GET http://localhost:8000/health
   ```

3. **API Documentation (Swagger UI)**
   ```bash
   GET http://localhost:8000/api/v1/docs
   ```

4. **OpenAPI Specification**
   ```bash
   GET http://localhost:8000/api/v1/openapi.json
   ```

5. **Create Opportunity**
   ```bash
   POST http://localhost:8000/api/v1/opportunities
   ```

6. **Get Opportunity Details**
   ```bash
   GET http://localhost:8000/api/v1/opportunities/{opportunity_id}
   ```

7. **Search Opportunities**
   ```bash
   GET http://localhost:8000/api/v1/opportunities?query=search&status=DRAFT
   ```

## Testing the API

### 1. Start the Server
```bash
cd opportunity_api
source venv/bin/activate
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Test Basic Endpoints
```bash
# Root endpoint
curl http://127.0.0.1:8000/

# Health check
curl http://127.0.0.1:8000/health

# Create an opportunity
curl -X POST "http://127.0.0.1:8000/api/v1/opportunities" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Opportunity",
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "customer_name": "Test Customer",
    "sales_manager_id": "123e4567-e89b-12d3-a456-426614174001",
    "description": "Test opportunity description",
    "priority": "HIGH",
    "annual_recurring_revenue": 50000.0,
    "geographic_requirements": {
      "region_id": "123e4567-e89b-12d3-a456-426614174002",
      "name": "North America",
      "requires_physical_presence": false,
      "allows_remote_work": true
    }
  }'
```

## Common Issues and Solutions

### Issue: Server won't start
**Check**: 
- Virtual environment is activated
- All dependencies are installed
- Port 8000 is not in use by another process

### Issue: Import errors
**Check**:
- All required packages are installed in the virtual environment
- Python path is correct
- No circular imports

### Issue: Database errors
**Check**:
- Database file permissions
- SQLite is available
- Database tables are created (happens automatically on startup)

### Issue: JSON serialization errors
**Check**:
- All UUID objects are converted to strings
- No datetime objects without proper serialization
- All custom objects have proper serialization methods

## Success Indicators

When everything is working correctly, you should see:

1. **Server startup logs**:
   ```
   INFO: Uvicorn running on http://127.0.0.1:8000
   INFO: Application startup complete.
   ```

2. **Successful API responses** with proper JSON structure:
   ```json
   {
     "data": { ... },
     "meta": {
       "timestamp": "2025-07-23T15:04:37.627701",
       "request_id": "c915c397-0687-45fe-9fe3-10e4e3b0f418"
     }
   }
   ```

3. **Interactive documentation** accessible at `http://127.0.0.1:8000/api/v1/docs`

## Next Steps

1. Visit the interactive documentation to explore all available endpoints
2. Use the provided curl examples to test different API operations
3. Check the main README.md for complete usage instructions
4. Review the API specification for detailed request/response schemas
