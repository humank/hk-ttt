# Step 7: Domain Model Diagram

This document provides a textual representation of the UML class diagram for the Opportunity Management Service domain model.

## UML Class Diagram (Textual Representation)

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

## Relationship Legend

- `<>-----` : Composition (filled diamond)
- `<>- - -` : Aggregation (empty diamond)
- `-------->` : Association with navigation
- `- - - - >` : Dependency

## Key Relationships

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

## Behavioral Notes

1. **Opportunity Lifecycle**:
   - Creation → Draft → Submission → Matching → Selection → Completion
   - Can be cancelled at any point before completion
   - Can be reactivated within 90 days if cancelled

2. **Validation Rules**:
   - Problem statement must meet minimum character requirement
   - At least one skill must be specified
   - Timeline must be valid (end date after start date)
   - All required fields must be complete before submission

3. **Modification Restrictions**:
   - No modifications allowed after a Solution Architect is selected
   - All modifications must be recorded in change history

## Business Rule Notes

1. **BR-8**: At least one "Must Have" skill must be specified
2. **BR-13**: Status transitions must follow the defined workflow
3. **BR-18**: Cancelled opportunities can be reactivated within 90 days
