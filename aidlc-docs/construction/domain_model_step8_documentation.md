# Step 8: Domain Model Documentation

This document provides comprehensive documentation for the Opportunity Management Service domain model, including descriptions of entities, attributes, behaviors, relationships, business rules, and how the model addresses each user story.

## Domain Model Overview

The Opportunity Management Service domain model is designed to support the complete lifecycle of customer opportunities, from creation to completion or cancellation. It enables Sales Managers to create detailed opportunity descriptions, specify required skills, manage timelines, track status, and make modifications as needed.

The model is centered around the `Opportunity` entity, which is composed of several related entities that capture different aspects of an opportunity:
- `ProblemStatement`: Detailed description of the customer's problem
- `SkillRequirement`: Technical skills, soft skills, industry knowledge required
- `TimelineRequirement`: Time-related requirements and constraints
- `OpportunityStatus`: Current state and status history
- `Attachment`: Supporting documents and files
- `ChangeRecord`: History of modifications for audit purposes

## Core Entities

### 1. Opportunity

The central entity representing a customer opportunity that requires a Solution Architect.

#### Description
The Opportunity entity captures the essential information about a customer's need for a Solution Architect. It serves as the aggregation root for all related entities and manages the overall lifecycle of the opportunity.

#### Key Attributes
- `id`: Unique identifier for the opportunity
- `title`: Title of the opportunity
- `customerId`: Reference to the customer
- `customerName`: Name of the customer
- `salesManagerId`: Reference to the Sales Manager who created it
- `description`: General description of the opportunity
- `priority`: Priority level (Low, Medium, High, Critical)
- `status`: Current status (Draft, Submitted, Matching in Progress, Matches Found, Architect Selected, Completed, Cancelled)
- `annualRecurringRevenue`: Expected ARR from the opportunity
- `geographicRequirements`: Geographic location requirements
- `createdAt`: When the opportunity was created
- `updatedAt`: When the opportunity was last updated
- `submittedAt`: When the opportunity was submitted for matching
- `completedAt`: When the opportunity was completed
- `cancelledAt`: When the opportunity was cancelled
- `cancellationReason`: Reason for cancellation if cancelled
- `reactivationDeadline`: Deadline for reactivating if cancelled (90 days after cancellation)

#### Key Behaviors
- `createOpportunity()`: Creates a new opportunity with initial status "Draft"
- `submitOpportunity()`: Validates and submits the opportunity for matching
- `updateOpportunity()`: Updates opportunity details with change tracking
- `cancelOpportunity()`: Cancels the opportunity with a reason
- `reactivateOpportunity()`: Reactivates a cancelled opportunity within the deadline
- `getStatus()`: Returns the current status
- `getChangeHistory()`: Returns the complete change history

#### Relationships
- Has one `ProblemStatement` (composition)
- Has many `SkillRequirement`s (composition)
- Has one `TimelineRequirement` (composition)
- Has many `OpportunityStatus` records (composition)
- Has many `ChangeRecord`s (composition)
- Created by one `User` (Sales Manager) (association)
- Associated with one `Customer` (association)

### 2. ProblemStatement

Detailed description of the customer's problem that needs to be solved.

#### Description
The ProblemStatement entity captures the comprehensive description of the customer's problem, supporting rich text formatting and attachments to provide additional context.

#### Key Attributes
- `id`: Unique identifier for the problem statement
- `opportunityId`: Reference to the opportunity
- `content`: Rich text content of the problem statement
- `minimumCharacterCount`: Minimum required character count
- `createdAt`: When the problem statement was created
- `updatedAt`: When the problem statement was last updated

#### Key Behaviors
- `createProblemStatement()`: Creates a new problem statement
- `updateContent()`: Updates the content with validation
- `validateContent()`: Validates content meets minimum requirements
- `previewContent()`: Returns formatted preview of the content

#### Relationships
- Part of one `Opportunity` (composition)
- Has many `Attachment`s (composition)

### 3. SkillRequirement

Represents a specific skill required for an opportunity.

#### Description
The SkillRequirement entity captures the skills needed for an opportunity, including technical skills, soft skills, industry knowledge, and languages, along with their importance and proficiency levels.

#### Key Attributes
- `id`: Unique identifier for the skill requirement
- `opportunityId`: Reference to the opportunity
- `skillId`: Reference to Skills Catalog
- `skillName`: Name of the skill
- `skillType`: Type of skill (Technical, Soft, Industry, Language)
- `importanceLevel`: Must Have, Nice to Have
- `minimumProficiencyLevel`: Beginner, Intermediate, Advanced, Expert
- `createdAt`: When the skill requirement was created
- `updatedAt`: When the skill requirement was last updated

#### Key Behaviors
- `createSkillRequirement()`: Creates a new skill requirement
- `updateImportanceLevel()`: Updates the importance level
- `updateProficiencyLevel()`: Updates the minimum proficiency level

#### Relationships
- Part of one `Opportunity` (composition)
- References one skill in the `Skills Catalog` (dependency)

### 4. TimelineRequirement

Represents the timeline specifications for an opportunity.

#### Description
The TimelineRequirement entity captures the time-related requirements for an opportunity, including start and end dates, specific required days, and flexibility information.

#### Key Attributes
- `id`: Unique identifier for the timeline requirement
- `opportunityId`: Reference to the opportunity
- `expectedStartDate`: Expected start date
- `expectedEndDate`: Expected end date
- `specificRequiredDays`: Specific days when SA is needed
- `isFlexible`: Whether the timeline is flexible
- `createdAt`: When the timeline requirement was created
- `updatedAt`: When the timeline requirement was last updated

#### Key Behaviors
- `createTimelineRequirement()`: Creates a new timeline requirement
- `updateDates()`: Updates start and end dates with validation
- `updateSpecificDays()`: Updates specific required days
- `updateFlexibility()`: Updates flexibility indicator
- `validateTimeline()`: Validates timeline information is complete and logical

#### Relationships
- Part of one `Opportunity` (composition)

### 5. OpportunityStatus

Represents the current status and status history of an opportunity.

#### Description
The OpportunityStatus entity captures the current state of an opportunity and maintains a history of status changes for tracking and audit purposes.

#### Key Attributes
- `id`: Unique identifier for the status record
- `opportunityId`: Reference to the opportunity
- `status`: Status value
- `changedAt`: When the status was changed
- `changedBy`: Reference to the user who changed the status
- `reason`: Reason for the status change

#### Key Behaviors
- `createStatusRecord()`: Creates a new status record
- `isValidTransition()`: Validates if a status transition is allowed
- `getStatusHistory()`: Returns complete status history for an opportunity

#### Relationships
- Part of one `Opportunity` (composition)
- Changed by one `User` (association)

### 6. Attachment

Represents a file attached to provide additional context.

#### Description
The Attachment entity captures metadata about files attached to a problem statement to provide additional context and information.

#### Key Attributes
- `id`: Unique identifier for the attachment
- `problemStatementId`: Reference to the problem statement
- `fileName`: Name of the file
- `fileType`: MIME type of the file
- `fileSize`: Size of the file in bytes
- `fileUrl`: URL to access the file
- `uploadedAt`: When the file was uploaded
- `uploadedBy`: Reference to the user who uploaded it

#### Key Behaviors
- `createAttachment()`: Creates a new attachment
- `removeAttachment()`: Marks attachment as removed

#### Relationships
- Part of one `ProblemStatement` (composition)
- Uploaded by one `User` (association)

### 7. ChangeRecord

Represents a change made to an opportunity for audit purposes.

#### Description
The ChangeRecord entity captures information about changes made to an opportunity, including what changed, when, by whom, and why, for audit and tracking purposes.

#### Key Attributes
- `id`: Unique identifier for the change record
- `opportunityId`: Reference to the opportunity
- `changedAt`: When the change was made
- `changedBy`: Reference to the user who made the change
- `fieldChanged`: Name of the field that was changed
- `oldValue`: Previous value
- `newValue`: New value
- `reason`: Reason for the change

#### Key Behaviors
- `createChangeRecord()`: Creates a new change record
- `getChangeHistory()`: Returns complete change history for an opportunity

#### Relationships
- Part of one `Opportunity` (composition)
- Made by one `User` (association)

## Key Business Rules

### Opportunity Creation and Validation
- BR-1: Required fields must be provided (customer name, title, description, start date, end date, priority, ARR)
- BR-2: System generates a unique ID for each opportunity
- BR-3: New opportunities are created with status "Draft"

### Problem Statement Requirements
- BR-4: Problem statement must meet minimum character requirement
- BR-5: Problem statement supports rich text formatting
- BR-6: Problem statement supports file attachments

### Skills Requirements
- BR-7: At least one skill must be specified
- BR-8: Each skill must have an importance level
- BR-9: Each skill must have a minimum proficiency level

### Timeline Management
- BR-10: Timeline must be valid (end date after start date)
- BR-11: Timeline uses end-date-based specification

### Status Tracking and Transitions
- BR-12: Status values follow a defined workflow
- BR-13: Status transitions must follow defined rules
- BR-14: Status changes are tracked with timestamp and user

### Opportunity Modification
- BR-15: No modifications allowed after a Solution Architect is selected
- BR-16: All modifications are recorded in change history

### Opportunity Cancellation and Reactivation
- BR-17: Cancellation requires a reason
- BR-18: Cancelled opportunities can be reactivated within 90 days

## User Story Implementation

### US-SM-3: Customer Opportunity Creation
**Implementation:**
- `Opportunity` entity with attributes for customer name, title, description, priority, ARR
- `createOpportunity()` method to create a new opportunity with initial status "Draft"
- Unique ID generation for each opportunity
- Validation of required fields

### US-SM-4: Problem Statement Documentation
**Implementation:**
- `ProblemStatement` entity with rich text content
- Minimum character requirement validation
- `Attachment` entity for supporting documents
- Preview functionality for problem statements

### US-SM-5: Required Skills Specification
**Implementation:**
- `SkillRequirement` entity for technical skills, soft skills, industry knowledge, languages
- Importance level (Must Have, Nice to Have) for each skill
- Minimum proficiency level for each skill
- References to Skills Catalog for standardized skills

### US-SM-6: Opportunity Timeline Management
**Implementation:**
- `TimelineRequirement` entity with start date, end date, specific days
- Flexibility indicator for timeline
- Validation of timeline logic (end date after start date)
- End-date-based specification as standardized approach

### US-SM-7: Opportunity Status Tracking
**Implementation:**
- `OpportunityStatus` entity to track current status and history
- Status values: Draft, Submitted, Matching in Progress, Matches Found, Architect Selected, Completed, Cancelled
- Status change tracking with timestamp and user
- Status transition rules enforcement

### US-SM-8: Opportunity Modification
**Implementation:**
- `updateOpportunity()` method with validation based on current status
- No modifications allowed after a Solution Architect is selected
- `ChangeRecord` entity to track all modifications
- Reason required for changes to submitted opportunities

### US-SM-9: Opportunity Cancellation
**Implementation:**
- `cancelOpportunity()` method with required reason
- Status change to "Cancelled"
- `reactivateOpportunity()` method with 90-day deadline
- Tracking of cancellation timestamp and reason

## Integration with Other Services

### User Management Service
- References `User` entity for Sales Manager authentication
- Uses `User` entity for tracking who made changes

### System Administration Service
- References `Skills Catalog` for standardized skills
- Uses shared data models for consistency

### Matching Engine Service
- Triggered when opportunities are submitted
- Provides opportunity details for matching

### Selection & Assignment Service
- Updates opportunity status when SAs are selected
- Receives status updates from opportunity lifecycle

## Conclusion

The domain model for the Opportunity Management Service provides a comprehensive foundation for implementing all the required user stories. It captures the complete lifecycle of opportunities from creation to completion or cancellation, with detailed tracking of problem statements, skill requirements, timelines, status changes, and modifications.

The model is designed to be flexible enough to accommodate the various requirements while enforcing important business rules and constraints. It integrates with shared components from the system's overall architecture and provides clear interfaces for interaction with other services.
