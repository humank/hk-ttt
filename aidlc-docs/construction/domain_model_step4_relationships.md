# Step 4: Entity Relationships

This document defines the relationships between entities in the Opportunity Management Service domain model.

## Relationship Types

The domain model uses the following relationship types:
- **Association**: Represents a relationship between two independent entities
- **Aggregation**: Represents a "has-a" relationship where the child can exist independently of the parent
- **Composition**: Represents a "part-of" relationship where the child cannot exist without the parent
- **Dependency**: Represents a "uses" relationship where one entity depends on another

## Entity Relationships

### 1. Opportunity Relationships

| Relationship | Target Entity | Type | Multiplicity | Description |
|--------------|--------------|------|-------------|-------------|
| has | ProblemStatement | Composition | 1..1 | An Opportunity has exactly one ProblemStatement; the ProblemStatement cannot exist without its Opportunity |
| has | SkillRequirement | Composition | 1..* | An Opportunity has one or more SkillRequirements; SkillRequirements cannot exist without their Opportunity |
| has | TimelineRequirement | Composition | 1..1 | An Opportunity has exactly one TimelineRequirement; the TimelineRequirement cannot exist without its Opportunity |
| has | OpportunityStatus | Composition | 1..* | An Opportunity has one or more status records (current and historical); status records cannot exist without their Opportunity |
| has | ChangeRecord | Composition | 0..* | An Opportunity has zero or more change records; change records cannot exist without their Opportunity |
| created by | User (Sales Manager) | Association | * → 1 | Many Opportunities can be created by one Sales Manager |
| associated with | Customer | Association | * → 1 | Many Opportunities can be associated with one Customer |

### 2. ProblemStatement Relationships

| Relationship | Target Entity | Type | Multiplicity | Description |
|--------------|--------------|------|-------------|-------------|
| part of | Opportunity | Composition | 1 → 1 | A ProblemStatement is part of exactly one Opportunity |
| has | Attachment | Composition | 0..* | A ProblemStatement has zero or more Attachments; Attachments cannot exist without their ProblemStatement |

### 3. SkillRequirement Relationships

| Relationship | Target Entity | Type | Multiplicity | Description |
|--------------|--------------|------|-------------|-------------|
| part of | Opportunity | Composition | * → 1 | Many SkillRequirements can be part of one Opportunity |
| references | Skills Catalog | Dependency | * → 1 | Many SkillRequirements can reference one skill in the Skills Catalog |

### 4. TimelineRequirement Relationships

| Relationship | Target Entity | Type | Multiplicity | Description |
|--------------|--------------|------|-------------|-------------|
| part of | Opportunity | Composition | 1 → 1 | A TimelineRequirement is part of exactly one Opportunity |

### 5. OpportunityStatus Relationships

| Relationship | Target Entity | Type | Multiplicity | Description |
|--------------|--------------|------|-------------|-------------|
| part of | Opportunity | Composition | * → 1 | Many status records can be part of one Opportunity (representing status history) |
| changed by | User | Association | * → 1 | Many status changes can be made by one User |

### 6. Attachment Relationships

| Relationship | Target Entity | Type | Multiplicity | Description |
|--------------|--------------|------|-------------|-------------|
| part of | ProblemStatement | Composition | * → 1 | Many Attachments can be part of one ProblemStatement |
| uploaded by | User | Association | * → 1 | Many Attachments can be uploaded by one User |

### 7. ChangeRecord Relationships

| Relationship | Target Entity | Type | Multiplicity | Description |
|--------------|--------------|------|-------------|-------------|
| part of | Opportunity | Composition | * → 1 | Many change records can be part of one Opportunity |
| made by | User | Association | * → 1 | Many changes can be made by one User |

## Relationship Diagrams

### Primary Relationships

```
User (Sales Manager) ◇──────────> Opportunity <──────────◇ Customer
                                     │
                                     │
                 ┌───────────────────┼───────────────────┐
                 │                   │                   │
                 ▼                   ▼                   ▼
         ProblemStatement    SkillRequirement    TimelineRequirement
                │                   │
                │                   │
                ▼                   ▼
           Attachment         Skills Catalog
```

### Tracking and History Relationships

```
Opportunity ◆───────────> OpportunityStatus <───────── User
     │
     │
     ▼
ChangeRecord <───────── User
```

## Key Relationship Constraints

1. **Opportunity Lifecycle**:
   - An Opportunity must have exactly one ProblemStatement
   - An Opportunity must have at least one SkillRequirement
   - An Opportunity must have exactly one TimelineRequirement
   - An Opportunity must have at least one OpportunityStatus record (current status)

2. **Deletion Constraints**:
   - Deleting an Opportunity cascades to delete all its composed entities (ProblemStatement, SkillRequirements, TimelineRequirement, OpportunityStatus records, and ChangeRecords)
   - Deleting a ProblemStatement cascades to delete all its Attachments
   - Users and Customers cannot be deleted if they are referenced by Opportunities

3. **Modification Constraints**:
   - After a Solution Architect is selected (status is "Architect Selected" or later), no modifications are allowed to the Opportunity or its composed entities
   - All modifications must be recorded in ChangeRecord entities
   - Status changes must follow the defined workflow transitions
