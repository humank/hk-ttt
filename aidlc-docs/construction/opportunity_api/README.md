# Opportunity Management Service API

A RESTful API for managing opportunities, problem statements, skill requirements, timeline requirements, and attachments.

## Features

- **Opportunity Management**: Create, submit, cancel, and reactivate opportunities
- **Problem Statements**: Add detailed problem descriptions to opportunities
- **Skill Requirements**: Define required skills with importance and proficiency levels
- **Timeline Requirements**: Set project timelines with flexibility options
- **File Attachments**: Upload and manage files for problem statements
- **Comprehensive Search**: Search opportunities with various filters
- **Audit Trail**: Track all changes with status and change history

## Technology Stack

- **Framework**: FastAPI
- **Database**: SQLite (configurable to PostgreSQL/MySQL)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Documentation**: Auto-generated OpenAPI/Swagger
- **Containerization**: Docker & Docker Compose

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Clone and navigate to the project directory**
   ```bash
   cd opportunity_api
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the API**
   - API Base URL: http://localhost:8000
   - Interactive Documentation: http://localhost:8000/api/v1/docs
   - Alternative Documentation: http://localhost:8000/api/v1/redoc

### Option 2: Local Development

1. **Run the startup script**
   ```bash
   ./start.sh
   ```

2. **Or manually:**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start the application
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

### Opportunities

- `POST /api/v1/opportunities` - Create a new opportunity
- `GET /api/v1/opportunities` - Search opportunities with filters
- `GET /api/v1/opportunities/{id}` - Get opportunity details
- `POST /api/v1/opportunities/{id}/submit` - Submit opportunity for matching
- `POST /api/v1/opportunities/{id}/cancel` - Cancel an opportunity
- `POST /api/v1/opportunities/{id}/reactivate` - Reactivate cancelled opportunity

### Problem Statements

- `POST /api/v1/opportunities/{id}/problem-statement` - Add problem statement

### Skill Requirements

- `POST /api/v1/opportunities/{id}/skill-requirements` - Add skill requirement

### Timeline Requirements

- `POST /api/v1/opportunities/{id}/timeline-requirement` - Add timeline requirement

### Attachments

- `POST /api/v1/problem-statements/{id}/attachments` - Upload attachment
- `GET /api/v1/problem-statements/{id}/attachments` - Get attachments
- `DELETE /api/v1/attachments/{id}` - Remove attachment
- `GET /api/v1/attachments/{id}/download` - Download attachment

### Health Check

- `GET /health` - Health check endpoint

## API Usage Examples

### Create an Opportunity

```bash
curl -X POST "http://localhost:8000/api/v1/opportunities" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Web Application Development",
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "customer_name": "Acme Corp",
    "sales_manager_id": "123e4567-e89b-12d3-a456-426614174001",
    "description": "Need to develop a modern web application",
    "priority": "HIGH",
    "annual_recurring_revenue": 100000.0,
    "geographic_requirements": {
      "region_id": "123e4567-e89b-12d3-a456-426614174002",
      "name": "North America",
      "requires_physical_presence": false,
      "allows_remote_work": true
    }
  }'
```

### Search Opportunities

```bash
curl "http://localhost:8000/api/v1/opportunities?status=DRAFT&priority=HIGH&page=1&page_size=10"
```

### Add Problem Statement

```bash
curl -X POST "http://localhost:8000/api/v1/opportunities/{opportunity_id}/problem-statement" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "We need to modernize our legacy system to improve user experience and reduce maintenance costs. The current system is built on outdated technology and lacks mobile responsiveness."
  }'
```

### Upload Attachment

```bash
curl -X POST "http://localhost:8000/api/v1/problem-statements/{problem_statement_id}/attachments" \
  -F "file=@document.pdf" \
  -F "uploaded_by=123e4567-e89b-12d3-a456-426614174001"
```

### Submit Opportunity

```bash
curl -X POST "http://localhost:8000/api/v1/opportunities/{opportunity_id}/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174001"
  }'
```

## Configuration

Configuration is managed through environment variables. Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
```

### Key Configuration Options

- `DATABASE_URL`: Database connection string
- `UPLOAD_DIR`: Directory for file uploads (default: ./uploads)
- `MAX_FILE_SIZE`: Maximum file size in bytes (default: 20MB)
- `ALLOWED_HOSTS`: CORS allowed origins
- `RATE_LIMIT_PER_MINUTE`: API rate limiting

## File Upload Configuration

- **Maximum file size**: 20MB (configurable)
- **Allowed file types**: All types (configurable)
- **Storage location**: ./uploads directory
- **File naming**: UUID-based to prevent conflicts

## Development

### Project Structure

```
opportunity_api/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   ├── opportunities.py
│   │   │   └── attachments.py
│   │   └── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   └── response.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── alembic/
├── tests/
├── uploads/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## Production Deployment

### Using Docker Compose with Nginx

```bash
# Start with production profile
docker-compose --profile production up -d
```

### Environment Variables for Production

```bash
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=["yourdomain.com"]
LOG_LEVEL=WARNING
```

## Monitoring and Health Checks

- **Health endpoint**: `/health`
- **Metrics**: Request ID tracking, response time logging
- **Rate limiting**: Configurable per-minute and per-hour limits
- **Error tracking**: Structured error responses with request IDs

## API Documentation

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## Error Handling

The API returns standardized error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid parameters",
    "details": [
      {
        "field": "title",
        "message": "Title is required"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-07-23T06:00:00Z",
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

## Performance Considerations

- **Response times**: <200ms for reads, <500ms for writes
- **Concurrent users**: Designed for 100 TPS/QPS, peak at 500 TPS/QPS
- **Rate limiting**: 100 requests per minute per IP
- **File uploads**: Streamed processing for large files
- **Database**: Connection pooling enabled

## Security Features

- **Input validation**: Pydantic model validation
- **File upload security**: Size and type restrictions
- **Rate limiting**: Per-IP request throttling
- **CORS**: Configurable cross-origin policies
- **Request tracking**: Unique request IDs for audit trails

## Support

For issues and questions:
1. Check the interactive API documentation at `/api/v1/docs`
2. Review the error response for detailed information
3. Check application logs for debugging information

## License

This project is part of the Opportunity Management Service system.
