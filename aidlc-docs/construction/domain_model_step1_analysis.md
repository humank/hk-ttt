# Step 1: User Stories Analysis

## Key Entities Identified

1. **Opportunity**
   - Central entity representing a customer opportunity
   - Referenced in all user stories (US-SM-3 through US-SM-9)

2. **Customer**
   - Entity representing the client for whom the opportunity exists
   - Referenced in US-SM-3

3. **Sales Manager**
   - User who creates and manages opportunities
   - Actor in all user stories

4. **Problem Statement**
   - Detailed description of the customer's problem
   - Referenced in US-SM-4

5. **Skill Requirement**
   - Technical skills, soft skills, industry knowledge required for an opportunity
   - Referenced in US-SM-5

6. **Timeline**
   - Time-related requirements for an opportunity
   - Referenced in US-SM-6

7. **Attachment**
   - Documents attached to provide additional context
   - Referenced in US-SM-4

8. **Status**
   - Current state of an opportunity in its lifecycle
   - Referenced in US-SM-7

9. **Change History**
   - Record of modifications made to an opportunity
   - Referenced in US-SM-8

## Attributes and Behaviors

### Opportunity
**Attributes:**
- ID (unique identifier)
- Customer name
- Title
- Description
- Problem statement
- Priority (Low, Medium, High, Critical)
- Status (Draft, Submitted, Matching in Progress, Matches Found, Architect Selected, Completed, Cancelled)
- Expected start date
- Expected end date
- Annual Recurring Revenue
- Required skills (technical, soft, industry, languages)
- Geographic requirements
- Timeline requirements
- Creation date
- Last updated date
- Cancellation reason (if applicable)

**Behaviors:**
- Create opportunity
- Submit opportunity for matching
- Update opportunity details
- Cancel opportunity
- Track status
- Reactivate cancelled opportunity (within 90 days)

### Problem Statement
**Attributes:**
- Content (rich text)
- Minimum character requirement
- Last updated date

**Behaviors:**
- Create/update problem statement
- Validate minimum length requirement
- Preview before submission

### Skill Requirement
**Attributes:**
- Skill type (Technical, Soft, Industry, Language)
- Skill ID (reference to Skills Catalog)
- Skill name
- Importance level (Must Have, Nice to Have)
- Geographic location requirements

**Behaviors:**
- Add skill requirement
- Remove skill requirement
- Update importance level

### Timeline
**Attributes:**
- Expected start date
- Expected end date
- Specific required days
- Flexibility indicator

**Behaviors:**
- Set timeline requirements
- Validate timeline logic

### Attachment
**Attributes:**
- File name
- File type
- File size
- Upload date
- Uploaded by

**Behaviors:**
- Upload attachment
- Remove attachment
- Download attachment

### Status
**Attributes:**
- Current status value
- Status change date
- Status change reason

**Behaviors:**
- Update status
- Track status history

### Change History
**Attributes:**
- Changed field
- Previous value
- New value
- Change date
- Changed by
- Change reason

**Behaviors:**
- Record change
- View change history

## Business Rules and Constraints

1. **Opportunity Creation (US-SM-3)**
   - Required fields must be provided (customer name, title, description, expected start date, expected duration, ARR)
   - System generates a unique opportunity ID
   - Initial status is "Draft"

2. **Problem Statement (US-SM-4)**
   - Problem statement has a minimum character requirement
   - Rich text formatting is supported
   - Attachments can be added to provide additional context

3. **Skills Requirements (US-SM-5)**
   - At least one skill must be specified
   - Skills come from the Skills Catalog in the shared model
   - Each skill must have an importance level (Must Have, Nice to Have)

4. **Timeline Management (US-SM-6)**
   - Timeline uses end-date-based specification
   - Expected start date must be provided
   - Timeline information must be complete and logical (e.g., end date after start date)

5. **Status Tracking (US-SM-7)**
   - Opportunities progress through defined status values
   - Status changes are tracked with timestamps

6. **Opportunity Modification (US-SM-8)**
   - All details can be edited before a Solution Architect is selected
   - No modifications allowed after a Solution Architect is selected
   - Changes require a reason when made to submitted opportunities
   - Change history is maintained for audit purposes

7. **Opportunity Cancellation (US-SM-9)**
   - Opportunities can be cancelled at any stage before completion
   - Cancellation requires a reason
   - Cancelled opportunities can be reactivated within 90 days

## Relationships

1. **Opportunity to Customer**: An opportunity is associated with one customer
2. **Opportunity to Sales Manager**: An opportunity is created and managed by one Sales Manager
3. **Opportunity to Problem Statement**: An opportunity has one problem statement
4. **Opportunity to Skill Requirements**: An opportunity has multiple skill requirements
5. **Opportunity to Timeline**: An opportunity has one timeline
6. **Opportunity to Attachments**: An opportunity can have multiple attachments
7. **Opportunity to Status**: An opportunity has one current status and a history of status changes
8. **Opportunity to Change History**: An opportunity has a history of changes made to it
