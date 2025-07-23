# Step 6: Business Rules and Constraints

This document defines the business rules and constraints that govern the behavior of the Opportunity Management Service domain model.

## Opportunity Creation and Validation

### BR-1: Required Fields for Opportunity Creation
- Customer name must be provided
- Opportunity title must be provided
- Opportunity description must be provided
- Expected start date must be provided
- Expected end date must be provided
- Priority level must be specified
- Annual Recurring Revenue must be provided

### BR-2: Opportunity ID Generation
- System must generate a unique ID for each new opportunity
- ID format must be UUID to ensure global uniqueness

### BR-3: Initial Status
- New opportunities must be created with status "Draft"
- Only opportunities in "Draft" status can be modified without restrictions

## Problem Statement Requirements

### BR-4: Problem Statement Minimum Length
- Problem statement must contain a minimum number of characters
- The minimum character requirement must be enforced during validation

### BR-5: Rich Text Support
- Problem statement must support rich text formatting
- Supported formatting includes headings, lists, bold, italic, and links

### BR-6: Attachment Support
- Problem statement must support file attachments
- Supported file types must be defined and enforced
- Maximum file size must be defined and enforced

## Skills Requirements

### BR-7: Minimum Skill Requirement
- At least one skill must be specified for an opportunity
- Skills must come from the Skills Catalog (no custom skills)

### BR-8: Skill Importance Level
- Each skill must have an importance level specified (Must Have, Nice to Have)
- At least one "Must Have" skill must be specified

### BR-9: Skill Proficiency Level
- Each skill must have a minimum proficiency level specified (Beginner, Intermediate, Advanced, Expert)

## Timeline Management

### BR-10: Timeline Validation
- Expected end date must be after expected start date
- If specific required days are specified, they must fall within the start and end dates
- Timeline must be marked as flexible or fixed

### BR-11: Timeline Standardization
- Timeline uses end-date-based specification (as per clarification)

## Status Tracking and Transitions

### BR-12: Valid Status Values
- Valid status values are: Draft, Submitted, Matching in Progress, Matches Found, Architect Selected, Completed, Cancelled
- Status transitions must follow the defined workflow

### BR-13: Status Transition Rules
- Draft → Submitted: All required fields must be complete and valid
- Submitted → Matching in Progress: System-triggered when matching process starts
- Matching in Progress → Matches Found: System-triggered when matches are available
- Matches Found → Architect Selected: Sales Manager selects an architect
- Architect Selected → Completed: Opportunity is marked as completed
- Any status except Completed → Cancelled: Opportunity can be cancelled
- Cancelled → Previous status: Opportunity can be reactivated within 90 days

### BR-14: Status Change Tracking
- All status changes must be recorded with timestamp and user
- Status change reason must be provided for certain transitions (e.g., cancellation)

## Opportunity Modification

### BR-15: Modification Restrictions
- All opportunity details can be modified when status is "Draft"
- No modifications are allowed after a Solution Architect is selected (status is "Architect Selected" or later)
- Modifications to submitted opportunities require a reason

### BR-16: Change History
- All modifications must be recorded in the change history
- Change records must include field name, old value, new value, timestamp, user, and reason

## Opportunity Cancellation and Reactivation

### BR-17: Cancellation Requirements
- Cancellation reason must be provided
- Cancellation can occur at any stage before completion
- Cancellation sets the status to "Cancelled"

### BR-18: Reactivation Rules
- Cancelled opportunities can be reactivated within 90 days of cancellation
- Reactivation restores the previous status before cancellation
- After 90 days, reactivation is not allowed

## Notification Rules

### BR-19: Status Change Notifications
- Relevant stakeholders must be notified when significant status changes occur
- Matched Solution Architects must be notified if an opportunity is cancelled

## Data Integrity and Validation

### BR-20: Data Integrity Constraints
- Relationships between entities must maintain referential integrity
- Deleting an opportunity must cascade to delete all related entities
- Users and customers referenced by opportunities cannot be deleted

### BR-21: Field Validation Rules
- Text fields have maximum length constraints
- Dates must be valid and logical
- Enumerations must contain only defined values

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

## Business Rule Enforcement

The business rules are enforced through:

1. **Entity Validation**: Rules enforced within entity methods
2. **Service Layer Validation**: Rules enforced by service layer before persistence
3. **Database Constraints**: Rules enforced by database constraints
4. **Event Handlers**: Rules enforced through event handlers for complex workflows
