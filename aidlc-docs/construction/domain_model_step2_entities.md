# Step 2: Core Domain Entities

Based on the analysis of user stories and the shared model, the following core domain entities have been identified for the Opportunity Management Service:

## Primary Entities

1. **Opportunity**
   - Central entity representing a customer opportunity
   - Covers user stories US-SM-3 through US-SM-9
   - Core functionality of the Opportunity Management Service

2. **ProblemStatement**
   - Detailed description of the customer's problem
   - Addresses US-SM-4
   - Contains rich text content and supports attachments

3. **SkillRequirement**
   - Represents skills needed for an opportunity
   - Addresses US-SM-5
   - References skills from the Skills Catalog

4. **TimelineRequirement**
   - Represents timeline specifications for an opportunity
   - Addresses US-SM-6
   - Contains start/end dates and flexibility information

5. **OpportunityStatus**
   - Represents the current state of an opportunity
   - Addresses US-SM-7
   - Tracks status changes over time

6. **Attachment**
   - Represents documents attached to a problem statement
   - Addresses US-SM-4
   - Contains file metadata and content reference

7. **ChangeRecord**
   - Represents a change made to an opportunity
   - Addresses US-SM-8
   - Contains audit information about what changed and why

## Shared Components to Reuse

From the shared model, we will reuse:

1. **User Component Model**
   - Used to represent the Sales Manager who creates and manages opportunities
   - Contains basic user information like ID, name, email, role

2. **Opportunity Component Model**
   - Will be extended and adapted for our specific requirements
   - Already contains many of the attributes we need

3. **Skills Catalog Component Model**
   - Referenced by SkillRequirement to ensure standardized skills
   - Provides the predefined list of skills

## Entity Mapping to User Stories

| Entity | User Stories | Description |
|--------|-------------|-------------|
| Opportunity | US-SM-3, US-SM-7, US-SM-8, US-SM-9 | Core entity for opportunity creation, status tracking, modification, and cancellation |
| ProblemStatement | US-SM-4 | Supports detailed problem documentation with rich text |
| SkillRequirement | US-SM-5 | Manages technical skills, soft skills, industry knowledge, languages, and geographic requirements |
| TimelineRequirement | US-SM-6 | Handles timeline specifications and validation |
| OpportunityStatus | US-SM-7 | Tracks status changes throughout the opportunity lifecycle |
| Attachment | US-SM-4 | Supports document attachments for additional context |
| ChangeRecord | US-SM-8 | Maintains audit trail of changes for modification tracking |

## Entity Relationships Overview

- **Opportunity** is the central entity that aggregates or composes other entities
- **ProblemStatement** is part of an Opportunity
- **SkillRequirement** is associated with an Opportunity (multiple per opportunity)
- **TimelineRequirement** is part of an Opportunity
- **OpportunityStatus** represents the current state of an Opportunity
- **Attachment** is associated with a ProblemStatement (multiple per problem statement)
- **ChangeRecord** is associated with an Opportunity (multiple per opportunity)

## Notes on Entity Design Decisions

1. **ProblemStatement as Separate Entity**
   - Separated from Opportunity to encapsulate rich text formatting and attachment management
   - Allows for focused validation of minimum character requirements

2. **SkillRequirement as Collection**
   - Represents individual skill requirements rather than a single collection
   - Allows for detailed tracking of importance levels per skill

3. **TimelineRequirement as Separate Entity**
   - Encapsulates timeline validation logic
   - Standardizes on end-date-based specification as per clarification

4. **OpportunityStatus as Value Object**
   - Represents the current state and transition rules
   - Maintains history of status changes

5. **Attachment as Entity**
   - Represents file metadata and storage information
   - Supports the rich context requirements of problem statements

6. **ChangeRecord as Entity**
   - Supports audit requirements for opportunity modifications
   - Captures what changed, when, by whom, and why
