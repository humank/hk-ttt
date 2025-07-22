# Domain Model Plan for Opportunity Management Service

## Overview
This plan outlines the steps to design a comprehensive Domain Model for the Opportunity Management Service based on the user stories US-SM-3 through US-SM-9. The model will define all components, attributes, behaviors, and interactions needed to implement the business logic.

## Plan Steps

### Phase 1: Core Entity Analysis
- [ ] **Step 1.1**: Identify and define the primary domain entities from user stories
  - Analyze each user story to extract core business entities
  - Define the main Opportunity entity and its lifecycle
  - Identify supporting entities (Customer, Skills, Timeline, etc.)

- [ ] **Step 2.2**: Define entity relationships and associations
  - Map relationships between Opportunity and other entities
  - Define cardinality and ownership relationships
  - Identify aggregates and aggregate roots

### Phase 2: Attributes and Properties Definition
- [ ] **Step 2.1**: Define Opportunity entity attributes
  - Core identification attributes (ID, title, description)
  - Business attributes (ARR, priority, status)
  - Temporal attributes (dates, duration, timeline)
  - Reference attributes (customer, sales manager)

- [ ] **Step 2.2**: Define Skills Requirements attributes
  - Technical skills with importance levels
  - Soft skills with importance levels
  - Industry knowledge requirements
  - Language and geographic requirements
  - Custom skills handling

- [ ] **Step 2.3**: Define supporting entity attributes
  - Customer entity attributes
  - Timeline entity attributes
  - Status history attributes
  - Document attachment attributes

### Phase 3: Behaviors and Business Logic
- [ ] **Step 3.1**: Define Opportunity lifecycle behaviors
  - Creation and validation logic
  - Status transition rules and constraints
  - Modification rules based on current status
  - Cancellation and reactivation logic

- [ ] **Step 3.2**: Define Skills Requirements behaviors
  - Skills validation and categorization
  - Importance level assignment logic
  - Custom skills addition and approval
  - Skills matching preparation logic

- [ ] **Step 3.3**: Define Timeline Management behaviors
  - Timeline validation logic
  - Availability checking logic
  - Timeline flexibility handling
  - Timeline update impact assessment

### Phase 4: Domain Services and Business Rules
- [ ] **Step 4.1**: Define domain services for complex business logic
  - Opportunity validation service
  - Skills matching preparation service
  - Timeline conflict detection service
  - Status transition orchestration service

- [ ] **Step 4.2**: Define business rules and constraints
  - Opportunity creation validation rules
  - Modification permission rules
  - Status transition constraints
  - Data integrity rules

### Phase 5: Integration and Event Handling
- [ ] **Step 5.1**: Define domain events
  - Opportunity created event
  - Opportunity modified event
  - Opportunity cancelled event
  - Status changed event

- [ ] **Step 5.2**: Define integration points with external services
  - User Management Service integration
  - Skills Catalog integration
  - Matching Engine Service triggers
  - Selection & Assignment Service updates

### Phase 6: Value Objects and Enumerations
- [ ] **Step 6.1**: Define value objects
  - Priority enumeration (Low, Medium, High, Critical)
  - Status enumeration (Draft, Submitted, Matching in Progress, etc.)
  - Skill importance levels (Must Have, Nice to Have)
  - Timeline flexibility indicators

- [ ] **Step 6.2**: Define complex value objects
  - Skills requirement value object
  - Timeline specification value object
  - Geographic requirement value object
  - Language requirement value object

### Phase 7: Documentation and Validation
- [ ] **Step 7.1**: Create comprehensive domain model documentation
  - Entity relationship diagrams
  - Behavior flow descriptions
  - Business rule specifications
  - Integration point definitions

- [ ] **Step 7.2**: Validate model against user stories
  - Verify each user story can be implemented with the model
  - Check acceptance criteria coverage
  - Validate business logic completeness

## Questions for Clarification

[Question] Should the Customer entity be fully defined within this domain model, or should it reference an external Customer Management Service?
[Answer] No

[Question] What is the expected behavior when a Sales Manager tries to modify an opportunity after a Solution Architect has been selected? Should certain fields become read-only?
[Answer] Yes

[Question] For the Skills Requirements, should we support skill hierarchies (e.g., AWS -> AWS Lambda -> Advanced Lambda Patterns) or keep them flat?
[Answer] Keep it flat

[Question] Should the system support multiple problem statements per opportunity, or is it always one problem statement per opportunity?
[Answer] It is always one problem statement per opportunity

[Question] For document attachments, what are the file size limits and supported file types?
[Answer] 20mb, any type of files are accepted.

[Question] Should the opportunity cancellation support partial cancellation (e.g., reducing scope) or only complete cancellation?
[Answer] No,no,no

[Question] What is the "defined timeframe" mentioned in US-SM-9 for reactivating cancelled opportunities?
[Answer] 90 days

[Question] Should the system support opportunity templates or cloning from previous similar opportunities?
[Answer] Cloning

## Success Criteria
- All user stories (US-SM-3 through US-SM-9) can be fully implemented using the domain model
- The model supports all acceptance criteria specified in the user stories
- Clear separation of concerns between entities, value objects, and domain services
- Well-defined integration points with external services
- Comprehensive business rule coverage
- Maintainable and extensible design

## Deliverables
- Complete domain model documentation in `domain_model.md`
- Entity relationship diagrams (textual representation)
- Business logic flow descriptions
- Integration specifications
