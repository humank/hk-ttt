# Step 5: Incorporate Shared Components

This document describes how shared components from `shared_model.md` are incorporated into the Opportunity Management Service domain model.

## Shared Components Used

From the shared model, we incorporate the following components:

1. **User Component Model**
2. **Opportunity Component Model**
3. **Skills Catalog Component Model**

## 1. User Component Model

The User Component Model is used as-is to represent Sales Managers who create and manage opportunities.

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

### Integration Points

- The `User` entity is referenced by the `Opportunity` entity through the `salesManagerId` attribute
- The `User` entity is referenced by the `OpportunityStatus` entity through the `changedBy` attribute
- The `User` entity is referenced by the `Attachment` entity through the `uploadedBy` attribute
- The `User` entity is referenced by the `ChangeRecord` entity through the `changedBy` attribute

### Constraints

- Only users with the role "SalesManager" can create and manage opportunities
- The user must be active (`isActive = true`) to perform operations on opportunities

## 2. Opportunity Component Model

The Opportunity Component Model from the shared model is adapted and extended for our specific requirements. We reuse the following structure:

```
## 3. Opportunity Component Model

The Opportunity component represents a customer opportunity that requires a Solution Architect.

### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the opportunity | Yes |
| title | String | Title of the opportunity | Yes |
| customerId | UUID | Reference to the customer | Yes |
| customerName | String | Name of the customer | Yes |
| salesManagerId | UUID | Reference to the Sales Manager who created it | Yes |
| description | String | General description of the opportunity | Yes |
| problemStatement | String | Detailed problem statement | Yes |
| priority | Enum | Priority level (Low, Medium, High, Critical) | Yes |
| status | Enum | Current status (Draft, Submitted, Matching, MatchesFound, ArchitectSelected, Completed, Cancelled) | Yes |
| annualRecurringRevenue | Decimal | Expected ARR from the opportunity | No |
| requiredTechnicalSkills | Array of RequiredSkill | Technical skills needed | Yes |
| requiredSoftSkills | Array of RequiredSkill | Soft skills needed | No |
| requiredIndustryKnowledge | Array of RequiredIndustry | Industry knowledge needed | No |
| requiredLanguages | Array of RequiredLanguage | Languages needed | No |
| geographicRequirements | Object | Geographic location requirements | Yes |
| timeline | Object | Timeline requirements | Yes |
| attachments | Array of Attachment | Related documents | No |
| createdAt | DateTime | When the opportunity was created | Yes |
| updatedAt | DateTime | When the opportunity was last updated | Yes |
| submittedAt | DateTime | When the opportunity was submitted for matching | No |
| completedAt | DateTime | When the opportunity was completed | No |
| changeHistory | Array of ChangeRecord | History of changes | Yes |
```

### Adaptations and Extensions

1. **Structural Changes**:
   - Extracted `problemStatement` into a separate `ProblemStatement` entity
   - Extracted `requiredTechnicalSkills`, `requiredSoftSkills`, `requiredIndustryKnowledge`, and `requiredLanguages` into a separate `SkillRequirement` entity
   - Extracted `timeline` into a separate `TimelineRequirement` entity
   - Extracted `attachments` to be associated with `ProblemStatement` instead of directly with `Opportunity`
   - Extracted `changeHistory` into a separate `ChangeRecord` entity
   - Added `cancelledAt`, `cancellationReason`, and `reactivationDeadline` attributes to support opportunity cancellation and reactivation

2. **Behavioral Extensions**:
   - Added methods for opportunity lifecycle management (create, submit, update, cancel, reactivate)
   - Added validation logic for required fields and business rules
   - Added status transition management

### Integration Points

- The `Opportunity` entity is the central entity in our domain model
- It composes or aggregates all other entities in the model
- It follows the same basic structure as the shared model but with more granular entity separation

## 3. Skills Catalog Component Model

The Skills Catalog Component Model is used as a reference for skill requirements. We reuse the following structure:

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

### Integration Points

- The `SkillRequirement` entity references the Skills Catalog through the `skillId` attribute
- All skills used in opportunities must come from the Skills Catalog (as per clarification)
- Only active skills (`isActive = true`) can be selected for opportunities

## Summary of Shared Component Integration

1. **Direct Reuse**:
   - `User` component is used as-is
   - `Skills Catalog` component is used as-is as a reference

2. **Adapted and Extended**:
   - `Opportunity` component is adapted and extended with more granular entity separation and additional attributes/behaviors

3. **Integration Strategy**:
   - Maintain consistency with shared models while providing the specific functionality needed for the Opportunity Management Service
   - Use references to shared components rather than duplicating their functionality
   - Extend shared components only where necessary to meet specific requirements
