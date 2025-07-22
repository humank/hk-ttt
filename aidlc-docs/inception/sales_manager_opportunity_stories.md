# User Stories: Sales Manager Opportunity Registration

## Account Management

### US-SM-1: Sales Manager Account Creation
**As a** Sales Manager,  
**I want to** create an account in the system,  
**So that** I can register customer opportunities and find matching Solution Architects.

**Acceptance Criteria:**
- Sales Manager can access a registration page
- Required fields include: name, email, employee ID, department, job title
- System validates email format and uniqueness
- System sends a verification email with account activation link
- Sales Manager receives confirmation upon successful registration
- Sales Manager can log in after account activation

### US-SM-2: Sales Manager Profile Management
**As a** Sales Manager,  
**I want to** manage my profile information,  
**So that** my contact details and team information are up-to-date.

**Acceptance Criteria:**
- Sales Manager can view their current profile information
- Sales Manager can edit their profile details
- Sales Manager can update their contact information
- Sales Manager can add/update their team information
- System saves changes and displays confirmation message
- Updated information is immediately reflected in the system

## Opportunity Registration

### US-SM-3: Customer Opportunity Creation
**As a** Sales Manager,  
**I want to** create a new customer opportunity in the system,  
**So that** I can find a suitable Solution Architect to address the customer's needs.

**Acceptance Criteria:**
- Sales Manager can access an opportunity creation form
- Required fields include: customer name, opportunity title, opportunity description, expected start date, expected duration
- Sales Manager can specify opportunity priority (Low, Medium, High, Critical)
- Sales Manager can associate the opportunity with an existing customer or create a new customer
- System generates a unique opportunity ID
- Sales Manager receives confirmation when opportunity is created successfully
- New opportunity appears in the Sales Manager's dashboard

### US-SM-4: Problem Statement Documentation
**As a** Sales Manager,  
**I want to** document a detailed problem statement for each opportunity,  
**So that** the system can match the most appropriate Solution Architects based on required skills.

**Acceptance Criteria:**
- Sales Manager can enter a comprehensive problem statement
- Sales Manager can use rich text formatting for better readability
- Sales Manager can attach relevant documents to provide additional context
- System provides guidance on creating effective problem statements
- Problem statement has a minimum character requirement to ensure sufficient detail
- Sales Manager can preview and edit the problem statement before submission

### US-SM-5: Required Skills Specification
**As a** Sales Manager,  
**I want to** specify the technical skills, soft skills, industry knowledge, languages, and geographic requirements for an opportunity,  
**So that** the system can find Solution Architects with matching capabilities.

**Acceptance Criteria:**
- Sales Manager can select required technical skills from a predefined list
- Sales Manager can select required soft skills from a predefined list
- Sales Manager can select required industry knowledge from a predefined list
- Sales Manager can specify required languages and proficiency levels
- Sales Manager can specify geographic location requirements
- Sales Manager can indicate the importance level of each skill (Must Have, Nice to Have)
- Sales Manager can add custom skills not found in the predefined lists
- System validates that at least one skill is specified

### US-SM-6: Opportunity Timeline Management
**As a** Sales Manager,  
**I want to** specify the timeline requirements for an opportunity,  
**So that** the system can match Solution Architects who are available during that period.

**Acceptance Criteria:**
- Sales Manager can specify the expected start date for the opportunity
- Sales Manager can specify the expected duration or end date
- Sales Manager can indicate specific days when the Solution Architect is needed
- Sales Manager can specify if the timeline is flexible or fixed
- System validates that the timeline information is complete and logical
- Sales Manager can update timeline information if changes occur

### US-SM-7: Opportunity Status Tracking
**As a** Sales Manager,  
**I want to** track the status of my registered opportunities,  
**So that** I know which opportunities have been matched with Solution Architects and which are still pending.

**Acceptance Criteria:**
- Sales Manager can view a list of all their registered opportunities
- Each opportunity displays its current status (Draft, Submitted, Matching in Progress, Matches Found, Architect Selected, Completed, Cancelled)
- Sales Manager can filter opportunities by status, date, customer, or other criteria
- Sales Manager can sort opportunities by various attributes
- System provides visual indicators for opportunities requiring attention
- Sales Manager can view detailed status history for each opportunity

### US-SM-8: Opportunity Modification
**As a** Sales Manager,  
**I want to** modify opportunity details after creation,  
**So that** I can update information as requirements change or new information becomes available.

**Acceptance Criteria:**
- Sales Manager can edit all opportunity details before a Solution Architect is selected
- Sales Manager can make limited changes after a Solution Architect is selected
- System maintains a change history for audit purposes
- System notifies relevant stakeholders when significant changes are made
- Sales Manager must provide a reason when making changes to submitted opportunities
- Updated information is immediately reflected in the matching algorithm

### US-SM-9: Opportunity Cancellation
**As a** Sales Manager,  
**I want to** cancel an opportunity if it's no longer needed,  
**So that** Solution Architects aren't matched to unnecessary opportunities.

**Acceptance Criteria:**
- Sales Manager can cancel an opportunity at any stage before completion
- Sales Manager must provide a reason for cancellation
- System notifies any already-matched Solution Architects about the cancellation
- Cancelled opportunities are marked accordingly but remain in the system for reporting
- Sales Manager can reactivate a cancelled opportunity within a defined timeframe
