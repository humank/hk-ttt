# Selection & Assignment Service

## Unit Overview
This service manages the workflow of viewing recommendations, making selections, and assigning Solution Architects to opportunities. It handles the complete selection process including notifications and post-selection activities.

## Scope and Responsibilities
- Display and manage match recommendations
- Handle Solution Architect selection process
- Manage assignment workflow and notifications
- Update availability and opportunity status
- Track selection history and decisions

## User Stories

### US-SS-1: View Recommended Solution Architects
**As a** Sales Manager,  
**I want to** view a list of recommended Solution Architects for my opportunity,  
**So that** I can select the most appropriate one for the customer.

**Acceptance Criteria:**
- Sales Manager receives notification when matches are found
- Sales Manager can access a dedicated page showing all recommended Solution Architects
- Recommendations are displayed in order of match score (highest to lowest)
- Each recommendation shows the Solution Architect's name, photo, match score, key skills, and availability
- System indicates when recommendations are ready within 1 hour of opportunity submission
- Sales Manager can refresh recommendations if needed

### US-SS-2: View Solution Architect Profiles
**As a** Sales Manager,  
**I want to** view detailed profiles of recommended Solution Architects,  
**So that** I can evaluate their qualifications beyond the match score.

**Acceptance Criteria:**
- Sales Manager can click on a recommendation to view the full profile
- Profile includes professional background, skills, experience, languages, and geographic expertise
- Profile highlights the specific skills that match the opportunity requirements
- Profile shows the Solution Architect's availability calendar for the opportunity timeline
- Sales Manager can navigate between profiles easily
- Profile includes any previous collaboration history with the Sales Manager or customer

### US-SS-4: Select a Solution Architect
**As a** Sales Manager,  
**I want to** select a Solution Architect for my opportunity,  
**So that** the customer can be served by the most appropriate professional.

**Acceptance Criteria:**
- Sales Manager can select any Solution Architect from the recommendations
- System prompts for confirmation before finalizing the selection
- Sales Manager can add notes explaining the selection decision
- System records the selection with timestamp and Sales Manager information
- Sales Manager receives confirmation when selection is complete
- Selected Solution Architect is clearly marked in the opportunity details

### US-SS-7: Notify Selected Solution Architect
**As the** system,  
**I want to** notify the selected Solution Architect via email with the Sales Manager in cc,  
**So that** they are aware of their assignment to the opportunity.

**Acceptance Criteria:**
- System automatically sends email notification to the selected Solution Architect
- Email includes the Sales Manager in cc
- Notification contains opportunity details, customer information, and next steps
- Notification includes a link to view the full opportunity in the system
- Solution Architect can acknowledge receipt of the notification
- System records when the notification was sent and acknowledged

## Key Capabilities
- **Recommendation Display**: Present match results in user-friendly format
- **Profile Integration**: Seamless access to detailed SA profiles
- **Selection Workflow**: Guided selection process with confirmation
- **Assignment Management**: Complete assignment lifecycle tracking
- **Notification System**: Automated notifications for selections and assignments
- **Status Updates**: Real-time updates to opportunity and availability status
- **Decision Tracking**: Maintain history of selection decisions and rationale

## Integration Points
- **Outbound Dependencies**: 
  - Matching Engine Service for recommendation data
  - Solution Architect Profile & Skills Service for detailed profiles and availability updates
  - Opportunity Management Service for status updates
  - User Management Service for user authentication
  - Email service for assignment notifications
- **Inbound Dependencies**: 
  - Sales Managers access this service to view recommendations and make selections
  - Matching Engine Service provides match results to this service
- **Shared Data Models**: 
  - Selection decisions and history
  - Assignment records
  - Notification status and acknowledgments
  - Opportunity-SA assignment relationships

## API Contracts
- Recommendation display endpoints
- Profile viewing endpoints
- Selection and assignment endpoints
- Notification management endpoints
- Assignment status tracking endpoints
- Selection history endpoints

## Notes
- Designed as a microservice with its own database for selection and assignment data
- Orchestrates the selection workflow across multiple services
- Includes comprehensive notification system for assignment communications
- Maintains selection history for analytics and audit purposes
- Updates availability and opportunity status in real-time
- Provides user-friendly interfaces for recommendation review and selection
- Handles the critical business process of SA assignment
