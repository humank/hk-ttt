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

---

# Python Implementation Plan

## Overview
This section outlines the steps to create a simple and intuitive Python implementation of the domain model components. The implementation will use a flat directory structure with individual files for each class, in-memory repositories, and standard Python libraries.

## Implementation Steps

### Phase 8: Enumerations and Value Objects Implementation
- [x] **Step 8.1**: Create enumeration classes
  - Create `priority.py` for Priority enum (Low, Medium, High, Critical)
  - Create `status.py` for OpportunityStatus enum (Draft, Submitted, Matching in Progress, etc.)
  - Create `skill_importance.py` for SkillImportance enum (Must Have, Nice to Have)
  - Create `timeline_flexibility.py` for TimelineFlexibility enum

- [x] **Step 8.2**: Create value object classes
  - Create `skill_requirement.py` for SkillRequirement value object
  - Create `timeline_specification.py` for TimelineSpecification value object
  - Create `geographic_requirement.py` for GeographicRequirement value object
  - Create `language_requirement.py` for LanguageRequirement value object
  - Create `document_attachment.py` for DocumentAttachment value object

### Phase 9: Core Entity Implementation
- [x] **Step 9.1**: Create entity base classes
  - Create `base_entity.py` with common entity functionality (ID, timestamps, etc.)
  - Create `aggregate_root.py` extending base entity with domain event support

- [x] **Step 9.2**: Create main entities
  - Create `customer.py` for Customer entity
  - Create `opportunity.py` for Opportunity entity (aggregate root)
  - Create `problem_statement.py` for ProblemStatement entity
  - Create `status_history.py` for StatusHistory entity

### Phase 10: Domain Services Implementation
- [x] **Step 10.1**: Create validation services
  - Create `opportunity_validation_service.py` for opportunity validation logic
  - Create `timeline_validation_service.py` for timeline validation logic
  - Create `skills_validation_service.py` for skills validation logic

- [x] **Step 10.2**: Create business logic services
  - Create `status_transition_service.py` for status transition orchestration
  - Create `opportunity_modification_service.py` for modification rules
  - Create `skills_matching_preparation_service.py` for matching preparation

### Phase 11: Domain Events Implementation
- [x] **Step 11.1**: Create event base classes
  - Create `domain_event.py` for base domain event class
  - Create `event_dispatcher.py` for event handling

- [x] **Step 11.2**: Create specific domain events
  - Create `opportunity_created_event.py`
  - Create `opportunity_modified_event.py`
  - Create `opportunity_cancelled_event.py`
  - Create `status_changed_event.py`

### Phase 12: Repository Implementation
- [x] **Step 12.1**: Create repository interfaces
  - Create `opportunity_repository.py` with abstract base class
  - Create `customer_repository.py` with abstract base class

- [x] **Step 12.2**: Create in-memory repository implementations
  - Create `in_memory_opportunity_repository.py`
  - Create `in_memory_customer_repository.py`

### Phase 13: Application Services Implementation
- [x] **Step 13.1**: Create application service classes
  - Create `opportunity_application_service.py` for orchestrating use cases
  - Create `opportunity_query_service.py` for read operations

### Phase 14: Utilities and Common Components
- [x] **Step 14.1**: Create utility classes
  - Create `exceptions.py` for custom domain exceptions
  - Create `validators.py` for common validation utilities
  - Create `date_utils.py` for date/time utilities

### Phase 15: Testing and Validation
- [x] **Step 15.1**: Create simple test examples
  - Create `test_opportunity_creation.py` to demonstrate opportunity creation
  - Create `test_status_transitions.py` to demonstrate status transitions
  - Create `test_skills_management.py` to demonstrate skills requirements

- [x] **Step 15.2**: Create usage examples
  - Create `example_usage.py` demonstrating the complete workflow
  - Create `README.md` with implementation overview and usage instructions

## Implementation Questions

[Question] Should we use Python dataclasses, Pydantic models, or regular classes for the entities and value objects?
[Answer] use Python dataclasses, Pydantic models

[Question] Do you want to include type hints throughout the implementation?
[Answer] Yes

[Question] Should we implement a simple logging mechanism using Python's logging module?
[Answer] Yes

[Question] For the in-memory repositories, should we use simple dictionaries or implement a more sophisticated in-memory storage?
[Answer] simple dictionaries

[Question] Should we include basic serialization/deserialization methods (to/from dict) for the entities?
[Answer] yes

[Question] Do you want to implement a simple dependency injection mechanism or keep dependencies explicit?
[Answer] simple dependency injection mechanism

[Question] Should we create a simple factory pattern for creating entities with proper validation?
[Answer] Yes

## Implementation Guidelines
- Keep the implementation simple and intuitive
- Use flat directory structure with one class per file
- Leverage standard Python libraries (datetime, uuid, enum, logging, etc.)
- Implement in-memory repositories using dictionaries
- Focus on readability and maintainability
- Include docstrings for all classes and methods
- Use meaningful variable and method names
- Implement proper error handling with custom exceptions

## Success Criteria for Implementation
- All domain model components are implemented in Python
- Code is simple, readable, and well-documented
- In-memory repositories work correctly
- Domain events are properly handled
- Business rules and validations are enforced
- All user story scenarios can be executed
- Code follows Python best practices
