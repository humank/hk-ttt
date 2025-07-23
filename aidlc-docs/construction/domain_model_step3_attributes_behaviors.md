# Step 3: Entity Attributes and Behaviors

This document defines the attributes and behaviors for each entity in the Opportunity Management Service domain model.

## 1. Opportunity

### Attributes

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

### Behaviors

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

## 2. ProblemStatement

### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the problem statement | Yes |
| opportunityId | UUID | Reference to the opportunity | Yes |
| content | String | Rich text content of the problem statement | Yes |
| minimumCharacterCount | Integer | Minimum required character count | Yes |
| createdAt | DateTime | When the problem statement was created | Yes |
| updatedAt | DateTime | When the problem statement was last updated | Yes |

### Behaviors

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

## 3. SkillRequirement

### Attributes

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

### Behaviors

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

## 4. TimelineRequirement

### Attributes

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

### Behaviors

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

## 5. OpportunityStatus

### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the status record | Yes |
| opportunityId | UUID | Reference to the opportunity | Yes |
| status | Enum | Status value (Draft, Submitted, Matching in Progress, Matches Found, Architect Selected, Completed, Cancelled) | Yes |
| changedAt | DateTime | When the status was changed | Yes |
| changedBy | UUID | Reference to the user who changed the status | Yes |
| reason | String | Reason for the status change | No |

### Behaviors

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

## 6. Attachment

### Attributes

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

### Behaviors

```
createAttachment(problemStatementId, fileName, fileType, fileSize, fileUrl, uploadedBy)
    Generates unique ID
    Sets upload timestamp
    Returns new Attachment

removeAttachment()
    Marks attachment as removed
    Does not physically delete the file for audit purposes
```

## 7. ChangeRecord

### Attributes

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

### Behaviors

```
createChangeRecord(opportunityId, changedBy, fieldChanged, oldValue, newValue, reason)
    Generates unique ID
    Sets timestamp
    Returns new ChangeRecord

getChangeHistory(opportunityId)
    Returns complete change history for an opportunity
```
