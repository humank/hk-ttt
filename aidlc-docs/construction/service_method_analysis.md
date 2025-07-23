# Service Method Analysis

## OpportunityService Methods Analysis

### 1. create_opportunity
**Purpose**: Create a new opportunity
**Parameters**:
- title: str
- customer_id: uuid.UUID
- customer_name: str
- sales_manager_id: uuid.UUID
- description: str
- priority: Priority (enum)
- annual_recurring_revenue: float
- geographic_requirements: Dict[str, Any]

**Returns**: Opportunity
**HTTP Mapping**: POST /api/v1/opportunities
**Request Schema**: OpportunityCreateRequest
**Response Schema**: OpportunityResponse

### 2. add_problem_statement
**Purpose**: Add a problem statement to an opportunity
**Parameters**:
- opportunity_id: uuid.UUID
- content: str

**Returns**: ProblemStatement
**HTTP Mapping**: POST /api/v1/opportunities/{id}/problem-statement
**Request Schema**: ProblemStatementCreateRequest
**Response Schema**: ProblemStatementResponse

### 3. add_skill_requirement
**Purpose**: Add a skill requirement to an opportunity
**Parameters**:
- opportunity_id: uuid.UUID
- skill_id: uuid.UUID
- skill_type: SkillType (enum)
- importance_level: ImportanceLevel (enum)
- minimum_proficiency_level: ProficiencyLevel (enum)

**Returns**: SkillRequirement
**HTTP Mapping**: POST /api/v1/opportunities/{id}/skill-requirements
**Request Schema**: SkillRequirementCreateRequest
**Response Schema**: SkillRequirementResponse

### 4. add_timeline_requirement
**Purpose**: Add a timeline requirement to an opportunity
**Parameters**:
- opportunity_id: uuid.UUID
- start_date: str
- end_date: str
- is_flexible: bool
- specific_days: Optional[List[str]]

**Returns**: TimelineRequirement
**HTTP Mapping**: POST /api/v1/opportunities/{id}/timeline-requirement
**Request Schema**: TimelineRequirementCreateRequest
**Response Schema**: TimelineRequirementResponse

### 5. submit_opportunity
**Purpose**: Submit an opportunity for matching
**Parameters**:
- opportunity_id: uuid.UUID
- user_id: uuid.UUID

**Returns**: Opportunity
**HTTP Mapping**: POST /api/v1/opportunities/{id}/submit
**Request Schema**: OpportunitySubmitRequest
**Response Schema**: OpportunityResponse

### 6. cancel_opportunity
**Purpose**: Cancel an opportunity
**Parameters**:
- opportunity_id: uuid.UUID
- user_id: uuid.UUID
- reason: str

**Returns**: Opportunity
**HTTP Mapping**: POST /api/v1/opportunities/{id}/cancel
**Request Schema**: OpportunityCancelRequest
**Response Schema**: OpportunityResponse

### 7. reactivate_opportunity
**Purpose**: Reactivate a cancelled opportunity
**Parameters**:
- opportunity_id: uuid.UUID
- user_id: uuid.UUID

**Returns**: Opportunity
**HTTP Mapping**: POST /api/v1/opportunities/{id}/reactivate
**Request Schema**: OpportunityReactivateRequest
**Response Schema**: OpportunityResponse

### 8. get_opportunity_details
**Purpose**: Get comprehensive details about an opportunity
**Parameters**:
- opportunity_id: uuid.UUID

**Returns**: Dict[str, Any]
**HTTP Mapping**: GET /api/v1/opportunities/{id}
**Request Schema**: None (path parameter only)
**Response Schema**: OpportunityDetailsResponse

### 9. search_opportunities
**Purpose**: Search for opportunities with various filters
**Parameters**:
- query: str = None
- status: str = None
- priority: str = None
- sales_manager_id: uuid.UUID = None
- customer_id: uuid.UUID = None

**Returns**: List[Opportunity]
**HTTP Mapping**: GET /api/v1/opportunities
**Request Schema**: None (query parameters)
**Response Schema**: OpportunityListResponse

## AttachmentService Methods Analysis

### 1. add_attachment
**Purpose**: Add an attachment to a problem statement
**Parameters**:
- problem_statement_id: uuid.UUID
- file_name: str
- file_type: str
- file_size: int
- file_url: str
- uploaded_by: uuid.UUID

**Returns**: Attachment
**HTTP Mapping**: POST /api/v1/problem-statements/{id}/attachments
**Request Schema**: AttachmentCreateRequest (multipart/form-data)
**Response Schema**: AttachmentResponse

### 2. remove_attachment
**Purpose**: Remove an attachment
**Parameters**:
- attachment_id: uuid.UUID
- user_id: uuid.UUID

**Returns**: Attachment
**HTTP Mapping**: DELETE /api/v1/attachments/{id}
**Request Schema**: AttachmentRemoveRequest
**Response Schema**: AttachmentResponse

### 3. get_attachments_for_problem_statement
**Purpose**: Get all attachments for a problem statement
**Parameters**:
- problem_statement_id: uuid.UUID

**Returns**: List[Attachment]
**HTTP Mapping**: GET /api/v1/problem-statements/{id}/attachments
**Request Schema**: None (path parameter only)
**Response Schema**: AttachmentListResponse

## API Endpoint Summary

### Opportunity Endpoints
1. POST /api/v1/opportunities - Create opportunity
2. GET /api/v1/opportunities/{id} - Get opportunity details
3. GET /api/v1/opportunities - Search opportunities
4. POST /api/v1/opportunities/{id}/submit - Submit opportunity
5. POST /api/v1/opportunities/{id}/cancel - Cancel opportunity
6. POST /api/v1/opportunities/{id}/reactivate - Reactivate opportunity
7. POST /api/v1/opportunities/{id}/problem-statement - Add problem statement
8. POST /api/v1/opportunities/{id}/skill-requirements - Add skill requirement
9. POST /api/v1/opportunities/{id}/timeline-requirement - Add timeline requirement

### Attachment Endpoints
1. POST /api/v1/problem-statements/{id}/attachments - Add attachment
2. GET /api/v1/problem-statements/{id}/attachments - Get attachments
3. DELETE /api/v1/attachments/{id} - Remove attachment

### Additional Endpoints (for file serving)
1. GET /api/v1/attachments/{id}/download - Download attachment file
2. GET /api/v1/health - Health check endpoint

## Request/Response Schema Requirements

### Common Schemas
- StandardResponse: Wrapper for all API responses
- ErrorResponse: Standard error response format
- PaginationResponse: For paginated results

### Opportunity Schemas
- OpportunityCreateRequest
- OpportunityResponse
- OpportunityDetailsResponse
- OpportunityListResponse
- OpportunitySubmitRequest
- OpportunityCancelRequest
- OpportunityReactivateRequest

### Problem Statement Schemas
- ProblemStatementCreateRequest
- ProblemStatementResponse

### Skill Requirement Schemas
- SkillRequirementCreateRequest
- SkillRequirementResponse

### Timeline Requirement Schemas
- TimelineRequirementCreateRequest
- TimelineRequirementResponse

### Attachment Schemas
- AttachmentCreateRequest
- AttachmentResponse
- AttachmentListResponse
- AttachmentRemoveRequest

## Authentication Considerations
Since authentication is set to "None", we'll skip user authentication but still need to handle user_id parameters in the service methods. We'll need to decide how to handle these:

1. **Option 1**: Remove user_id parameters and skip authorization checks
2. **Option 2**: Accept user_id as request parameter without validation
3. **Option 3**: Use a default/mock user_id for all operations

**Recommendation**: Use Option 2 - accept user_id as request parameter for operations that require it, but skip authentication validation.
