# Step 1: Analyze Service Requirements

## Methods to be Exposed

Based on the analysis of `services.py`, the following methods need to be exposed:

### OpportunityService

1. `create_opportunity`
   - Purpose: Create a new opportunity
   - Input: title, customer_id, customer_name, sales_manager_id, description, priority, annual_recurring_revenue, geographic_requirements
   - Output: Opportunity object
   - Authorization: Sales Manager role

2. `add_problem_statement`
   - Purpose: Add a problem statement to an opportunity
   - Input: opportunity_id, content
   - Output: ProblemStatement object
   - Authorization: Sales Manager role (owner of the opportunity)

3. `add_skill_requirement`
   - Purpose: Add a skill requirement to an opportunity
   - Input: opportunity_id, skill_id, skill_type, importance_level, minimum_proficiency_level
   - Output: SkillRequirement object
   - Authorization: Sales Manager role (owner of the opportunity)

4. `add_timeline_requirement`
   - Purpose: Add a timeline requirement to an opportunity
   - Input: opportunity_id, start_date, end_date, is_flexible, specific_days (optional)
   - Output: TimelineRequirement object
   - Authorization: Sales Manager role (owner of the opportunity)

5. `submit_opportunity`
   - Purpose: Submit an opportunity for matching
   - Input: opportunity_id, user_id
   - Output: Updated Opportunity object
   - Authorization: Sales Manager role (owner of the opportunity) or Admin role

6. `cancel_opportunity`
   - Purpose: Cancel an opportunity
   - Input: opportunity_id, user_id, reason
   - Output: Updated Opportunity object
   - Authorization: Sales Manager role (owner of the opportunity) or Admin role

7. `reactivate_opportunity`
   - Purpose: Reactivate a cancelled opportunity
   - Input: opportunity_id, user_id
   - Output: Updated Opportunity object
   - Authorization: Sales Manager role (owner of the opportunity) or Admin role

8. `get_opportunity_details`
   - Purpose: Get comprehensive details about an opportunity
   - Input: opportunity_id
   - Output: Dictionary with opportunity details
   - Authorization: Sales Manager role (owner of the opportunity) or Admin role

9. `search_opportunities`
   - Purpose: Search for opportunities with various filters
   - Input: query (optional), status (optional), priority (optional), sales_manager_id (optional), customer_id (optional)
   - Output: List of Opportunity objects
   - Authorization: Sales Manager role or Admin role

### AttachmentService

1. `add_attachment`
   - Purpose: Add an attachment to a problem statement
   - Input: problem_statement_id, file_name, file_type, file_size, file_url, uploaded_by
   - Output: Attachment object
   - Authorization: Sales Manager role (owner of the opportunity)

2. `remove_attachment`
   - Purpose: Remove an attachment
   - Input: attachment_id, user_id
   - Output: Updated Attachment object
   - Authorization: Sales Manager role (owner of the opportunity) or Admin role

3. `get_attachments_for_problem_statement`
   - Purpose: Get all attachments for a problem statement
   - Input: problem_statement_id
   - Output: List of Attachment objects
   - Authorization: Sales Manager role (owner of the opportunity) or Admin role

## Authentication and Authorization Requirements

Based on the provided answers:

- **Authentication**: OAuth 2.0 with JWT tokens
- **Authorization**: Role-based access control with Sales Manager and Admin roles
- **Integration**: Existing Amazon Cognito user pool

Authorization rules:
1. Sales Managers can only access and modify their own opportunities
2. Admins can access and modify any opportunity
3. All methods require authentication
4. Most write operations require specific role permissions

## Data Models and Serialization Needs

The following data models need to be serialized for API communication:

1. **Opportunity**: Core entity with opportunity details
2. **ProblemStatement**: Contains problem statement content
3. **SkillRequirement**: Contains skill requirement details
4. **TimelineRequirement**: Contains timeline requirement details
5. **Attachment**: Contains attachment metadata
6. **OpportunityStatus**: Contains status information
7. **ChangeRecord**: Contains change history information

Serialization considerations:
- UUID fields need to be converted to strings
- DateTime fields need to be converted to ISO 8601 format
- Enum values need to be converted to strings
- Complex objects need to be flattened for API responses

## Traffic Patterns and Performance Requirements

Based on the provided answers:

- **Traffic Volume**: 100 requests per second with peaks of up to 500 requests during business hours (9 AM - 5 PM EST)
- **Latency Requirements**: 
  - Read operations: < 200ms
  - Write operations: < 500ms
- **Data Volume**: Starting with 10GB, growing by 1GB per month
- **Deployment Frequency**: Weekly for features, daily for critical bug fixes

## Compliance Requirements

- **GDPR Compliance**: Required as the service will store data of EU citizens
  - Need to implement data protection measures
  - Need to support data subject rights (access, rectification, erasure)
  - Need to implement data minimization and purpose limitation
  - Need to maintain records of processing activities

## Integration Requirements

- **Amazon Cognito**: For user authentication and authorization
- **Amazon RDS**: For data persistence

## Summary of Requirements

1. **API Type**: Public API with authentication and authorization
2. **Authentication**: OAuth 2.0 with JWT tokens via Amazon Cognito
3. **Authorization**: Role-based access control (Sales Manager and Admin roles)
4. **Performance**: Handle 500 RPS at peak with low latency responses
5. **Compliance**: GDPR compliance required
6. **Integration**: Existing Cognito user pool and RDS database
7. **Deployment**: Support for frequent deployments (daily/weekly)
8. **Data Growth**: Moderate data growth (1GB/month)
