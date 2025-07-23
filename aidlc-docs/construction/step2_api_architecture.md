# Step 2: Choose API Architecture

## REST vs GraphQL Evaluation

### REST API

**Advantages:**
- Widely adopted and understood
- Excellent caching capabilities
- Stateless nature fits well with serverless architecture
- Better support for file uploads (important for attachment handling)
- Simpler to implement and maintain
- Better tooling support in AWS (API Gateway)

**Disadvantages:**
- Multiple endpoints may lead to over-fetching or under-fetching data
- Multiple round trips might be needed for complex data requirements
- Versioning can be challenging

### GraphQL API

**Advantages:**
- Clients can request exactly the data they need
- Single endpoint for all operations
- Strong typing and introspection
- Reduces over-fetching and under-fetching
- Versioning is more flexible

**Disadvantages:**
- More complex to implement
- Caching is more challenging
- File uploads are not natively supported
- Performance monitoring can be more difficult
- Authorization can be more complex to implement

### Decision

Based on the requirements and considerations:

**REST API is the recommended choice** for the following reasons:
1. The service has well-defined operations that map naturally to REST endpoints
2. File upload functionality is required for attachments
3. The performance requirements (< 200ms for reads, < 500ms for writes) favor REST's caching capabilities
4. Integration with existing AWS services (Cognito, RDS) is more straightforward with REST
5. The team's familiarity with REST will likely lead to faster implementation and fewer issues

## API Endpoints and Operations

### OpportunityService Endpoints

1. **Opportunities Resource**
   - `POST /opportunities` - Create a new opportunity
   - `GET /opportunities` - Search opportunities with filters
   - `GET /opportunities/{id}` - Get opportunity details
   - `POST /opportunities/{id}/submit` - Submit an opportunity
   - `POST /opportunities/{id}/cancel` - Cancel an opportunity
   - `POST /opportunities/{id}/reactivate` - Reactivate an opportunity

2. **Problem Statements Resource**
   - `POST /opportunities/{id}/problem-statement` - Add a problem statement

3. **Skill Requirements Resource**
   - `POST /opportunities/{id}/skill-requirements` - Add a skill requirement
   - `GET /opportunities/{id}/skill-requirements` - Get skill requirements for an opportunity

4. **Timeline Requirements Resource**
   - `POST /opportunities/{id}/timeline-requirement` - Add a timeline requirement
   - `GET /opportunities/{id}/timeline-requirement` - Get timeline requirement for an opportunity

### AttachmentService Endpoints

1. **Attachments Resource**
   - `POST /problem-statements/{id}/attachments` - Add an attachment
   - `GET /problem-statements/{id}/attachments` - Get attachments for a problem statement
   - `DELETE /attachments/{id}` - Remove an attachment

## Request/Response Formats

### Standard Response Format

All API responses will follow a standard format:

```json
{
  "data": {
    // Response data specific to the endpoint
  },
  "meta": {
    "timestamp": "2025-07-23T04:00:00Z",
    "requestId": "550e8400-e29b-41d4-a716-446655440000"
  },
  "pagination": {
    // Pagination information (when applicable)
    "page": 1,
    "pageSize": 10,
    "totalItems": 100,
    "totalPages": 10
  }
}
```

### Error Response Format

Error responses will follow a standard format:

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
    "timestamp": "2025-07-23T04:00:00Z",
    "requestId": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### Data Type Mapping

| Python Type | JSON Type | Format/Notes |
|-------------|-----------|--------------|
| uuid.UUID | string | UUID format |
| datetime | string | ISO 8601 format |
| Enum | string | Enum value as string |
| float | number | Decimal number |
| int | number | Integer |
| bool | boolean | true/false |
| None | null | null |
| List | array | JSON array |
| Dict | object | JSON object |

## Error Handling Approach

### Error Categories

1. **Validation Errors (400 Bad Request)**
   - Missing required fields
   - Invalid field values
   - Business rule violations

2. **Authentication Errors (401 Unauthorized)**
   - Missing authentication token
   - Invalid authentication token
   - Expired authentication token

3. **Authorization Errors (403 Forbidden)**
   - Insufficient permissions
   - Role-based access control violations

4. **Resource Not Found Errors (404 Not Found)**
   - Requested resource does not exist

5. **Conflict Errors (409 Conflict)**
   - Resource already exists
   - Concurrent modification conflicts

6. **Server Errors (500 Internal Server Error)**
   - Unexpected exceptions
   - Database errors
   - Integration errors

### Error Codes

Each error will have a specific error code that provides more detail about the error:

- `VALIDATION_ERROR`: Request validation failed
- `AUTHENTICATION_ERROR`: Authentication failed
- `AUTHORIZATION_ERROR`: Authorization failed
- `RESOURCE_NOT_FOUND`: Resource not found
- `RESOURCE_ALREADY_EXISTS`: Resource already exists
- `OPERATION_NOT_ALLOWED`: Operation not allowed in current state
- `INTERNAL_ERROR`: Internal server error

### Exception Mapping

| Domain Exception | HTTP Status | Error Code |
|------------------|-------------|------------|
| ValidationException | 400 | VALIDATION_ERROR |
| NotFoundException | 404 | RESOURCE_NOT_FOUND |
| OperationNotAllowedException | 403 | OPERATION_NOT_ALLOWED |
| Other exceptions | 500 | INTERNAL_ERROR |

## API Documentation

The API will be documented using the OpenAPI Specification (formerly Swagger) to provide:

1. Comprehensive endpoint documentation
2. Request and response schemas
3. Authentication requirements
4. Example requests and responses

This documentation will be made available through a Swagger UI interface for easy exploration and testing of the API.

## API Versioning Strategy

The API will use URL versioning to ensure backward compatibility:

- `/api/v1/opportunities`
- `/api/v1/problem-statements`

This approach allows for introducing breaking changes in future versions while maintaining support for existing clients.

## Rate Limiting and Throttling

To protect the API from abuse and ensure fair usage:

1. Implement rate limiting at 1000 requests per minute per client
2. Implement throttling to handle traffic spikes
3. Return appropriate 429 Too Many Requests responses when limits are exceeded
4. Include rate limit information in response headers:
   - `X-RateLimit-Limit`: Maximum requests per minute
   - `X-RateLimit-Remaining`: Remaining requests in the current window
   - `X-RateLimit-Reset`: Time when the rate limit resets
