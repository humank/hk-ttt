# Opportunity Management Service Domain Model

## Overview

This document defines the domain model for the Opportunity Management Service, which handles all Sales Manager activities related to creating, managing, and tracking customer opportunities. The model supports the complete lifecycle of opportunities from creation to completion or cancellation.

## Core Domain Entities

### 1. Opportunity

The central entity representing a customer opportunity that requires a Solution Architect.

#### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the opportunity | Yes |
| title | String | Title of the opportunity | Yes |
| customerId | UUID | Reference to the customer | Yes |
| customerName | String | Name of the customer | Yes |
| salesManagerId | UUID | Reference to the Sales Manager who created it | Yes |
| description | String | General description of the opportunity | Yes |
| priority | Enum | Priority level (Low, Medium, High, Critical) | Yes |
| status | Enum | Current status (Draft, Submitted, Matching in Progress, Matches Found, Architect Selected, Completed, Cancelled) | Yes |
| annualRecurringRevenue | Decimal | Expected ARR from the opportunity | Yes |
| geographicRequirements | Object | Geographic location requirements | Yes |
| createdAt | DateTime | When the opportunity was created | Yes |
| updatedAt | DateTime | When the opportunity was last updated | Yes |
| submittedAt | DateTime | When the opportunity was submitted for matching | No |
| completedAt | DateTime | When the opportunity was completed | No |
| cancelledAt | DateTime | When the opportunity was cancelled | No |
| cancellationReason | String | Reason for cancellation if cancelled | No |
| reactivationDeadline | DateTime | Deadline for reactivating if cancelled (90 days after cancellation) | No |

#### Behaviors

```
createOpportunity(title, customerInfo, description, startDate, endDate, priority, annualRecurringRevenue)
    Validates required fields
    Generates unique ID
    Sets initial status to Draft
    Sets creation timestamp
    Returns new Opportunity

submitOpportunity()
    Validates all required fields are complete
    Validates problem statement meets minimum length
    Validates at least one skill is specified
    Validates timeline information is complete
    Changes status to Submitted
    Sets submission timestamp
    Triggers matching process

updateOpportunity(field, newValue, reason)
    Validates modification is allowed based on current status
    If status is after "Architect Selected", throws OperationNotAllowedException
    Updates specified field with new value
    Records change in change history with reason
    Updates last modified timestamp

cancelOpportunity(reason)
    Validates cancellation reason is provided
    Changes status to Cancelled
    Sets cancellation timestamp
    Sets reactivation deadline to 90 days from now
    Notifies any matched Solution Architects

reactivateOpportunity()
    Validates opportunity is in Cancelled status
    Validates current date is before reactivation deadline
    Restores previous status before cancellation
    Clears cancellation-related fields
    Records change in change history

getStatus()
    Returns current status

getChangeHistory()
    Returns complete change history
```

### 2. ProblemStatement

Detailed description of the customer's problem that needs to be solved.

#### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the problem statement | Yes |
| opportunityId | UUID | Reference to the opportunity | Yes |
| content | String | Rich text content of the problem statement | Yes |
| minimumCharacterCount | Integer | Minimum required character count | Yes |
| createdAt | DateTime | When the problem statement was created | Yes |
| updatedAt | DateTime | When the problem statement was last updated | Yes |

#### Behaviors

```
createProblemStatement(opportunityId, content)
    Validates content meets minimum character requirement
    Generates unique ID
    Sets creation timestamp
    Returns new ProblemStatement

updateContent(newContent)
    Validates new content meets minimum character requirement
    Updates content
    Updates last modified timestamp

validateContent()
    Checks if content meets minimum character requirement
    Returns boolean result

previewContent()
    Returns formatted preview of the content
```

### 3. SkillRequirement

Represents a specific skill required for an opportunity.

#### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the skill requirement | Yes |
| opportunityId | UUID | Reference to the opportunity | Yes |
| skillId | UUID | Reference to Skills Catalog | Yes |
| skillName | String | Name of the skill | Yes |
| skillType | Enum | Type of skill (Technical, Soft, Industry, Language) | Yes |
| importanceLevel | Enum | Must Have, Nice to Have | Yes |
| minimumProficiencyLevel | Enum | Beginner, Intermediate, Advanced, Expert | Yes |
| createdAt | DateTime | When the skill requirement was created | Yes |
| updatedAt | DateTime | When the skill requirement was last updated | Yes |

#### Behaviors

```
createSkillRequirement(opportunityId, skillId, skillName, skillType, importanceLevel, minimumProficiencyLevel)
    Validates skill exists in Skills Catalog
    Generates unique ID
    Sets creation timestamp
    Returns new SkillRequirement

updateImportanceLevel(newLevel)
    Updates importance level
    Updates last modified timestamp

updateProficiencyLevel(newLevel)
    Updates minimum proficiency level
    Updates last modified timestamp
```

### 4. TimelineRequirement

Represents the timeline specifications for an opportunity.

#### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the timeline requirement | Yes |
| opportunityId | UUID | Reference to the opportunity | Yes |
| expectedStartDate | Date | Expected start date | Yes |
| expectedEndDate | Date | Expected end date | Yes |
| specificRequiredDays | Array of Date | Specific days when SA is needed | No |
| isFlexible | Boolean | Whether the timeline is flexible | Yes |
| createdAt | DateTime | When the timeline requirement was created | Yes |
| updatedAt | DateTime | When the timeline requirement was last updated | Yes |

#### Behaviors

```
createTimelineRequirement(opportunityId, startDate, endDate, isFlexible, specificDays)
    Validates end date is after start date
    Validates specific days fall within start and end dates
    Generates unique ID
    Sets creation timestamp
    Returns new TimelineRequirement

updateDates(startDate, endDate)
    Validates end date is after start date
    Updates start and end dates
    Updates last modified timestamp

updateSpecificDays(specificDays)
    Validates specific days fall within start and end dates
    Updates specific required days
    Updates last modified timestamp

updateFlexibility(isFlexible)
    Updates flexibility indicator
    Updates last modified timestamp

validateTimeline()
    Checks if timeline information is complete and logical
    Returns boolean result
```

### 5. OpportunityStatus

Represents the current status and status history of an opportunity.

#### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the status record | Yes |
| opportunityId | UUID | Reference to the opportunity | Yes |
| status | Enum | Status value (Draft, Submitted, Matching in Progress, Matches Found, Architect Selected, Completed, Cancelled) | Yes |
| changedAt | DateTime | When the status was changed | Yes |
| changedBy | UUID | Reference to the user who changed the status | Yes |
| reason | String | Reason for the status change | No |

#### Behaviors

```
createStatusRecord(opportunityId, status, changedBy, reason)
    Generates unique ID
    Sets timestamp
    Returns new OpportunityStatus

isValidTransition(currentStatus, newStatus)
    Validates if the transition from current to new status is allowed
    Returns boolean result

getStatusHistory(opportunityId)
    Returns complete status history for an opportunity
```

### 6. Attachment

Represents a file attached to provide additional context.

#### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the attachment | Yes |
| problemStatementId | UUID | Reference to the problem statement | Yes |
| fileName | String | Name of the file | Yes |
| fileType | String | MIME type of the file | Yes |
| fileSize | Integer | Size of the file in bytes | Yes |
| fileUrl | String | URL to access the file | Yes |
| uploadedAt | DateTime | When the file was uploaded | Yes |
| uploadedBy | UUID | Reference to the user who uploaded it | Yes |

#### Behaviors

```
createAttachment(problemStatementId, fileName, fileType, fileSize, fileUrl, uploadedBy)
    Generates unique ID
    Sets upload timestamp
    Returns new Attachment

removeAttachment()
    Marks attachment as removed
    Does not physically delete the file for audit purposes
```

### 7. ChangeRecord

Represents a change made to an opportunity for audit purposes.

#### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the change record | Yes |
| opportunityId | UUID | Reference to the opportunity | Yes |
| changedAt | DateTime | When the change was made | Yes |
| changedBy | UUID | Reference to the user who made the change | Yes |
| fieldChanged | String | Name of the field that was changed | Yes |
| oldValue | String | Previous value | No |
| newValue | String | New value | No |
| reason | String | Reason for the change | Yes |

#### Behaviors

```
createChangeRecord(opportunityId, changedBy, fieldChanged, oldValue, newValue, reason)
    Generates unique ID
    Sets timestamp
    Returns new ChangeRecord

getChangeHistory(opportunityId)
    Returns complete change history for an opportunity
```

## Shared Components

### 1. User Component Model

```
## 1. User Component Model

The User component represents basic user information across the system.

### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the user | Yes |
| name | String | Full name of the user | Yes |
| email | String | Email address (used for login) | Yes |
| role | Enum | User role in the system (SA, SalesManager, Admin) | Yes |
| employeeId | String | Company employee ID | Yes |
| department | String | Department or business unit | Yes |
| jobTitle | String | Official job title | Yes |
| isActive | Boolean | Whether the user account is active | Yes |
| createdAt | DateTime | When the user account was created | Yes |
| lastLoginAt | DateTime | When the user last logged in | No |
| profilePictureUrl | String | URL to profile picture | No |
| phoneNumber | String | Contact phone number | No |
```

### 2. Skills Catalog Component Model

```
## 4. Skills Catalog Component Model

The Skills Catalog component represents the standardized taxonomy of skills used throughout the system.

### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the skill | Yes |
| name | String | Name of the skill | Yes |
| category | Enum | Category (Technical, Soft, Industry, Language) | Yes |
| subcategory | String | Subcategory for organization | No |
| description | String | Description of the skill | Yes |
| isActive | Boolean | Whether the skill is active in the catalog | Yes |
| createdAt | DateTime | When the skill was added to the catalog | Yes |
| updatedAt | DateTime | When the skill was last updated | Yes |
| relatedSkills | Array of UUID | References to related skills | No |
| synonyms | Array of String | Alternative names for the skill | No |
```

## Entity Relationships

### Relationship Diagram (Textual Representation)

```
+------------------------+       +------------------------+       +------------------------+
|         User           |       |       Customer         |       |    Skills Catalog      |
+------------------------+       +------------------------+       +------------------------+
| id: UUID               |       | id: UUID               |       | id: UUID               |
| name: String           |       | name: String           |       | name: String           |
| email: String          |       | ...                    |       | category: Enum         |
| role: Enum             |       +------------------------+       | subcategory: String    |
| employeeId: String     |                                       | description: String     |
| department: String     |                                       | isActive: Boolean       |
| jobTitle: String       |                                       | ...                     |
| isActive: Boolean      |                                       +------------------------+
| ...                    |                                                  ▲
+------------------------+                                                  |
         ▲                                                                  |
         |                                                                  |
         |                                                                  |
+------------------------+       +------------------------+       +------------------------+
|     Opportunity        |       |   ProblemStatement     |       |   SkillRequirement    |
+------------------------+       +------------------------+       +------------------------+
| id: UUID               |<>-----| id: UUID               |       | id: UUID               |
| title: String          |       | opportunityId: UUID    |       | opportunityId: UUID    |
| customerId: UUID       |       | content: String        |       | skillId: UUID          |
| customerName: String   |       | minimumCharacterCount: |       | skillName: String      |
| salesManagerId: UUID   |       | createdAt: DateTime    |       | skillType: Enum        |
| description: String    |       | updatedAt: DateTime    |       | importanceLevel: Enum  |
| priority: Enum         |       | ...                    |       | minimumProficiency: Enum|
| status: Enum           |       +------------------------+       | ...                    |
| annualRecurringRevenue |               |                        +------------------------+
| geographicRequirements |               |                                  |
| createdAt: DateTime    |               |                                  |
| updatedAt: DateTime    |               |                                  |
| submittedAt: DateTime  |               |                                  |
| completedAt: DateTime  |               |                                  |
| cancelledAt: DateTime  |               |                                  |
| cancellationReason     |               |                                  |
| reactivationDeadline   |               |                                  |
+------------------------+               |                                  |
         |                               |                                  |
         |                               |                                  |
         |                               |                                  |
+------------------------+       +------------------------+       +------------------------+
| TimelineRequirement    |       |      Attachment        |<------| OpportunityStatus      |
+------------------------+       +------------------------+       +------------------------+
| id: UUID               |       | id: UUID               |       | id: UUID               |
| opportunityId: UUID    |       | problemStatementId: UUID|       | opportunityId: UUID    |
| expectedStartDate: Date|       | fileName: String       |       | status: Enum           |
| expectedEndDate: Date  |       | fileType: String       |       | changedAt: DateTime    |
| specificRequiredDays   |       | fileSize: Integer      |       | changedBy: UUID        |
| isFlexible: Boolean    |       | fileUrl: String        |       | reason: String         |
| ...                    |       | uploadedAt: DateTime   |       | ...                    |
+------------------------+       | uploadedBy: UUID       |       +------------------------+
                                 | ...                    |
                                 +------------------------+
                                           |
                                           |
                                           |
                                 +------------------------+
                                 |     ChangeRecord       |
                                 +------------------------+
                                 | id: UUID               |
                                 | opportunityId: UUID    |
                                 | changedAt: DateTime    |
                                 | changedBy: UUID        |
                                 | fieldChanged: String   |
                                 | oldValue: String       |
                                 | newValue: String       |
                                 | reason: String         |
                                 | ...                    |
                                 +------------------------+
```

### Key Relationships

1. **Opportunity to ProblemStatement**: Composition (1..1)
   - An Opportunity has exactly one ProblemStatement
   - ProblemStatement cannot exist without its Opportunity

2. **Opportunity to SkillRequirement**: Composition (1..*)
   - An Opportunity has one or more SkillRequirements
   - SkillRequirements cannot exist without their Opportunity

3. **Opportunity to TimelineRequirement**: Composition (1..1)
   - An Opportunity has exactly one TimelineRequirement
   - TimelineRequirement cannot exist without its Opportunity

4. **Opportunity to OpportunityStatus**: Composition (1..*)
   - An Opportunity has one or more status records
   - Status records cannot exist without their Opportunity

5. **Opportunity to ChangeRecord**: Composition (0..*)
   - An Opportunity has zero or more change records
   - Change records cannot exist without their Opportunity

6. **ProblemStatement to Attachment**: Composition (0..*)
   - A ProblemStatement has zero or more Attachments
   - Attachments cannot exist without their ProblemStatement

7. **SkillRequirement to Skills Catalog**: Dependency (*..*) 
   - SkillRequirements reference skills from the Skills Catalog

8. **Opportunity to User**: Association (*..*) 
   - Many Opportunities can be created by one User (Sales Manager)
   - One User can create many Opportunities

9. **Opportunity to Customer**: Association (*..*) 
   - Many Opportunities can be associated with one Customer
   - One Customer can have many Opportunities

## Business Rules and Constraints

### Opportunity Creation and Validation

1. **Required Fields for Opportunity Creation**
   - Customer name must be provided
   - Opportunity title must be provided
   - Opportunity description must be provided
   - Expected start date must be provided
   - Expected end date must be provided
   - Priority level must be specified
   - Annual Recurring Revenue must be provided

2. **Opportunity ID Generation**
   - System must generate a unique ID for each new opportunity
   - ID format must be UUID to ensure global uniqueness

3. **Initial Status**
   - New opportunities must be created with status "Draft"
   - Only opportunities in "Draft" status can be modified without restrictions

### Problem Statement Requirements

4. **Problem Statement Minimum Length**
   - Problem statement must contain a minimum number of characters
   - The minimum character requirement must be enforced during validation

5. **Rich Text Support**
   - Problem statement must support rich text formatting
   - Supported formatting includes headings, lists, bold, italic, and links

6. **Attachment Support**
   - Problem statement must support file attachments
   - Supported file types must be defined and enforced
   - Maximum file size must be defined and enforced

### Skills Requirements

7. **Minimum Skill Requirement**
   - At least one skill must be specified for an opportunity
   - Skills must come from the Skills Catalog (no custom skills)

8. **Skill Importance Level**
   - Each skill must have an importance level specified (Must Have, Nice to Have)
   - At least one "Must Have" skill must be specified

9. **Skill Proficiency Level**
   - Each skill must have a minimum proficiency level specified (Beginner, Intermediate, Advanced, Expert)

### Timeline Management

10. **Timeline Validation**
    - Expected end date must be after expected start date
    - If specific required days are specified, they must fall within the start and end dates
    - Timeline must be marked as flexible or fixed

11. **Timeline Standardization**
    - Timeline uses end-date-based specification (as per clarification)

### Status Tracking and Transitions

12. **Valid Status Values**
    - Valid status values are: Draft, Submitted, Matching in Progress, Matches Found, Architect Selected, Completed, Cancelled
    - Status transitions must follow the defined workflow

13. **Status Transition Rules**
    - Draft → Submitted: All required fields must be complete and valid
    - Submitted → Matching in Progress: System-triggered when matching process starts
    - Matching in Progress → Matches Found: System-triggered when matches are available
    - Matches Found → Architect Selected: Sales Manager selects an architect
    - Architect Selected → Completed: Opportunity is marked as completed
    - Any status except Completed → Cancelled: Opportunity can be cancelled
    - Cancelled → Previous status: Opportunity can be reactivated within 90 days

14. **Status Change Tracking**
    - All status changes must be recorded with timestamp and user
    - Status change reason must be provided for certain transitions (e.g., cancellation)

### Opportunity Modification

15. **Modification Restrictions**
    - All opportunity details can be modified when status is "Draft"
    - No modifications are allowed after a Solution Architect is selected (status is "Architect Selected" or later)
    - Modifications to submitted opportunities require a reason

16. **Change History**
    - All modifications must be recorded in the change history
    - Change records must include field name, old value, new value, timestamp, user, and reason

### Opportunity Cancellation and Reactivation

17. **Cancellation Requirements**
    - Cancellation reason must be provided
    - Cancellation can occur at any stage before completion
    - Cancellation sets the status to "Cancelled"

18. **Reactivation Rules**
    - Cancelled opportunities can be reactivated within 90 days of cancellation
    - Reactivation restores the previous status before cancellation
    - After 90 days, reactivation is not allowed

## State Transition Diagram

```
┌─────────┐         ┌───────────┐         ┌────────────────────┐
│  Draft  │────────>│ Submitted │────────>│ Matching in Progress│
└─────────┘         └───────────┘         └────────────────────┘
    │                     │                          │
    │                     │                          │
    │                     │                          ▼
    │                     │               ┌────────────────────┐
    │                     │               │   Matches Found    │
    │                     │               └────────────────────┘
    │                     │                          │
    │                     │                          │
    ▼                     ▼                          ▼
┌─────────┐         ┌───────────┐         ┌────────────────────┐
│Cancelled│<────────│ Completed │<────────│ Architect Selected │
└─────────┘         └───────────┘         └────────────────────┘
    │
    │ (within 90 days)
    ▼
Previous Status
```

## User Story Implementation

### US-SM-3: Customer Opportunity Creation
The domain model supports this user story through the `Opportunity` entity with attributes for customer name, title, description, priority, and ARR. The `createOpportunity()` method creates a new opportunity with initial status "Draft" and generates a unique ID. Required fields are validated during creation.

### US-SM-4: Problem Statement Documentation
The domain model supports this user story through the `ProblemStatement` entity with rich text content and minimum character requirement validation. The `Attachment` entity supports document attachments for additional context, and the `previewContent()` method provides preview functionality.

### US-SM-5: Required Skills Specification
The domain model supports this user story through the `SkillRequirement` entity for technical skills, soft skills, industry knowledge, and languages. Each skill has an importance level (Must Have, Nice to Have) and a minimum proficiency level. Skills are referenced from the Skills Catalog for standardization.

### US-SM-6: Opportunity Timeline Management
The domain model supports this user story through the `TimelineRequirement` entity with start date, end date, and specific days. The timeline can be marked as flexible or fixed, and validation ensures logical timeline information (end date after start date).

### US-SM-7: Opportunity Status Tracking
The domain model supports this user story through the `OpportunityStatus` entity to track current status and history. Status values include Draft, Submitted, Matching in Progress, Matches Found, Architect Selected, Completed, and Cancelled. Status changes are tracked with timestamp and user.

### US-SM-8: Opportunity Modification
The domain model supports this user story through the `updateOpportunity()` method with validation based on current status. No modifications are allowed after a Solution Architect is selected. The `ChangeRecord` entity tracks all modifications with reason, timestamp, and user.

### US-SM-9: Opportunity Cancellation
The domain model supports this user story through the `cancelOpportunity()` method with required reason. The status is changed to "Cancelled" and the cancellation timestamp and reason are recorded. The `reactivateOpportunity()` method allows reactivation within 90 days.

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
