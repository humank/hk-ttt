# Step 4: Design Authentication and Authorization

This document outlines the authentication and authorization design for the Opportunity Management Service API.

## Authentication Service Selection

Based on the requirements and the fact that we need to integrate with an existing Amazon Cognito user pool, we will use **Amazon Cognito** as our authentication service.

### Authentication Flow

We will implement the OAuth 2.0 authorization code flow with PKCE (Proof Key for Code Exchange) for secure authentication:

1. **Client Application Initiates Login**:
   - Redirects the user to the Cognito hosted UI or uses the Cognito SDK
   - Includes PKCE code challenge

2. **User Authentication**:
   - User enters credentials in the Cognito hosted UI
   - Cognito validates credentials against the user pool

3. **Authorization Code Return**:
   - Cognito returns an authorization code to the client application
   - Client exchanges the code for tokens using the PKCE code verifier

4. **Token Acquisition**:
   - Client receives ID token, access token, and refresh token
   - ID token contains user identity information
   - Access token is used for API authorization

5. **API Requests**:
   - Client includes the access token in the Authorization header
   - API Gateway validates the token before forwarding requests to the backend

6. **Token Refresh**:
   - Client uses the refresh token to obtain new access tokens when they expire
   - Reduces the need for users to re-authenticate frequently

### Token Configuration

1. **Access Token**:
   - JWT format
   - 1-hour expiration
   - Contains user ID, groups/roles, and custom claims
   - Signed with RS256 algorithm

2. **ID Token**:
   - JWT format
   - Contains user identity information
   - Used by the client application for user profile display

3. **Refresh Token**:
   - 30-day expiration
   - Used to obtain new access tokens
   - Revocable for security purposes

## Authorization Design

### Role-Based Access Control (RBAC)

Based on the requirements, we need to implement role-based access control with two primary roles:

1. **Sales Manager Role**:
   - Can create and manage their own opportunities
   - Can view their own opportunities
   - Can add problem statements, skill requirements, and timeline requirements to their opportunities
   - Can submit, cancel, and reactivate their own opportunities
   - Can add and remove attachments to their own problem statements

2. **Admin Role**:
   - Can view all opportunities
   - Can manage all opportunities (submit, cancel, reactivate)
   - Can add and remove attachments to any problem statement
   - Can perform administrative functions

### Authorization Rules

| Endpoint | Sales Manager | Admin |
|----------|--------------|-------|
| `POST /opportunities` | Create own opportunities | Create opportunities for any sales manager |
| `GET /opportunities` | View own opportunities | View all opportunities |
| `GET /opportunities/{id}` | View own opportunity | View any opportunity |
| `POST /opportunities/{id}/submit` | Submit own opportunity | Submit any opportunity |
| `POST /opportunities/{id}/cancel` | Cancel own opportunity | Cancel any opportunity |
| `POST /opportunities/{id}/reactivate` | Reactivate own opportunity | Reactivate any opportunity |
| `POST /opportunities/{id}/problem-statement` | Add to own opportunity | Add to any opportunity |
| `POST /opportunities/{id}/skill-requirements` | Add to own opportunity | Add to any opportunity |
| `GET /opportunities/{id}/skill-requirements` | View for own opportunity | View for any opportunity |
| `POST /opportunities/{id}/timeline-requirement` | Add to own opportunity | Add to any opportunity |
| `GET /opportunities/{id}/timeline-requirement` | View for own opportunity | View for any opportunity |
| `POST /problem-statements/{id}/attachments` | Add to own problem statement | Add to any problem statement |
| `GET /problem-statements/{id}/attachments` | View for own problem statement | View for any problem statement |
| `DELETE /attachments/{id}` | Remove from own problem statement | Remove from any problem statement |

### Token Validation and Handling

1. **API Gateway JWT Authorizer**:
   - Validates the JWT signature using Cognito's public keys
   - Verifies token expiration
   - Extracts user ID and roles from the token
   - Passes user context to the backend service

2. **Fine-Grained Authorization in the Service Layer**:
   - Implement ownership checks for Sales Managers
   - Implement role-based permission checks
   - Use the user ID and roles from the JWT token

3. **Token Handling in the Client**:
   - Store tokens securely (e.g., in memory, secure storage)
   - Include access token in the Authorization header
   - Handle token refresh when access tokens expire
   - Handle authentication errors and redirect to login when needed

## Custom Claims and Scopes

To support our authorization requirements, we will configure the following custom claims in the JWT tokens:

1. **`custom:role`**: User's role (SalesManager or Admin)
2. **`custom:department`**: User's department
3. **`custom:employeeId`**: User's employee ID

We will also define the following OAuth 2.0 scopes:

1. **`opportunity-service/read`**: Read access to opportunities
2. **`opportunity-service/write`**: Write access to opportunities
3. **`opportunity-service/admin`**: Administrative access

## API Gateway Authorization Configuration

1. **Cognito Authorizer**:
   - Configure API Gateway to use Cognito as an authorizer
   - Specify the Cognito user pool and app client
   - Configure token validation settings

2. **Resource-Level Authorization**:
   - Configure authorization at the resource and method level
   - Define which scopes are required for each endpoint

3. **Lambda Authorizer for Complex Rules**:
   - Implement a Lambda authorizer for complex authorization rules
   - Use the authorizer to validate ownership and permissions
   - Cache authorization results for performance

## Security Considerations

1. **Token Security**:
   - Use HTTPS for all API endpoints
   - Implement proper token storage in clients
   - Set appropriate token expiration times

2. **CORS Configuration**:
   - Configure CORS headers to allow only trusted domains
   - Implement proper preflight request handling

3. **Rate Limiting and Throttling**:
   - Implement rate limiting per user to prevent abuse
   - Configure different rate limits for different endpoints

4. **Audit Logging**:
   - Log all authentication and authorization events
   - Include user ID, IP address, and requested resource
   - Store logs in CloudWatch Logs with appropriate retention

## GDPR Compliance Considerations

1. **User Consent**:
   - Implement mechanisms to obtain and record user consent
   - Allow users to withdraw consent

2. **Data Access and Portability**:
   - Implement endpoints for users to access their personal data
   - Provide data in a portable format

3. **Right to be Forgotten**:
   - Implement mechanisms to delete user data upon request
   - Ensure deletion across all systems

4. **Data Minimization**:
   - Only collect and store necessary personal data
   - Implement data retention policies

## Implementation Approach

1. **Cognito User Pool Configuration**:
   - Configure the existing Cognito user pool
   - Set up app clients with appropriate settings
   - Configure custom attributes and scopes

2. **API Gateway Integration**:
   - Configure Cognito authorizers for API Gateway
   - Define authorization scopes for each endpoint

3. **Backend Service Implementation**:
   - Extract user information from the request context
   - Implement ownership and permission checks
   - Return appropriate error responses for unauthorized requests

4. **Client SDK Development**:
   - Create helper functions for authentication and token management
   - Implement automatic token refresh
   - Handle authentication errors gracefully
