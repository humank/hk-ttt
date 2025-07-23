# Opportunity Management Service

This is a Python implementation of the Opportunity Management Service domain model, which handles all Sales Manager activities related to creating, managing, and tracking customer opportunities.

## Overview

The Opportunity Management Service supports the complete lifecycle of opportunities from creation to completion or cancellation. It enables Sales Managers to create detailed opportunity descriptions, specify required skills, manage timelines, track status, and make modifications as needed.

## Features

- **Opportunity Creation**: Create new customer opportunities with detailed information
- **Problem Statement Documentation**: Document comprehensive problem statements with rich text support
- **Skills Requirements**: Specify technical skills, soft skills, industry knowledge, and languages needed
- **Timeline Management**: Define timeline requirements with start/end dates and specific days
- **Status Tracking**: Track opportunity status throughout its lifecycle
- **Opportunity Modification**: Update opportunity details with change tracking
- **Opportunity Cancellation**: Cancel opportunities with reason tracking and reactivation support
- **Event Notifications**: Publish events for key actions (creation, submission, cancellation, etc.)

## Architecture

The implementation follows a domain-driven design approach with the following components:

- **Entities**: Core domain objects with identity and lifecycle
- **Value Objects**: Immutable objects that describe characteristics of entities
- **Repositories**: Interfaces and implementations for data access
- **Services**: Coordinate between entities and repositories to implement business operations
- **Validators**: Enforce business rules and constraints
- **Events**: Publish and subscribe to domain events

## Directory Structure

```
opportunity_management_service/
├── __init__.py
├── attachment.py
├── base_entity.py
├── change_record.py
├── common.py
├── customer.py
├── enums.py
├── example.py
├── in_memory_repositories.py
├── opportunity.py
├── opportunity_status.py
├── problem_statement.py
├── repositories.py
├── services.py
├── skill_requirement.py
├── skills_catalog.py
├── tests.py
├── timeline_requirement.py
├── user.py
├── validators.py
└── value_objects.py
```

## Usage

### Basic Usage

```python
from opportunity_management_service.enums import Priority, SkillType, ImportanceLevel, ProficiencyLevel
from opportunity_management_service.in_memory_repositories import (
    InMemoryUserRepository, InMemoryCustomerRepository, InMemorySkillsCatalogRepository,
    InMemoryOpportunityRepository, InMemoryProblemStatementRepository, InMemorySkillRequirementRepository,
    InMemoryTimelineRequirementRepository, InMemoryOpportunityStatusRepository,
    InMemoryAttachmentRepository, InMemoryChangeRecordRepository
)
from opportunity_management_service.services import OpportunityService, AttachmentService

# Create repositories
user_repository = InMemoryUserRepository()
customer_repository = InMemoryCustomerRepository()
skills_catalog_repository = InMemorySkillsCatalogRepository()
opportunity_repository = InMemoryOpportunityRepository()
problem_statement_repository = InMemoryProblemStatementRepository()
skill_requirement_repository = InMemorySkillRequirementRepository()
timeline_requirement_repository = InMemoryTimelineRequirementRepository()
opportunity_status_repository = InMemoryOpportunityStatusRepository()
attachment_repository = InMemoryAttachmentRepository()
change_record_repository = InMemoryChangeRecordRepository()

# Create services
opportunity_service = OpportunityService(
    opportunity_repository=opportunity_repository,
    problem_statement_repository=problem_statement_repository,
    skill_requirement_repository=skill_requirement_repository,
    timeline_requirement_repository=timeline_requirement_repository,
    opportunity_status_repository=opportunity_status_repository,
    change_record_repository=change_record_repository,
    skills_catalog_repository=skills_catalog_repository,
    user_repository=user_repository,
    customer_repository=customer_repository
)

# Create an opportunity
opportunity = opportunity_service.create_opportunity(
    title="Cloud Migration Project",
    customer_id=customer_id,
    customer_name="Acme Inc.",
    sales_manager_id=sales_manager_id,
    description="Migrate on-premises infrastructure to the cloud",
    priority=Priority.HIGH,
    annual_recurring_revenue=100000.0,
    geographic_requirements={
        "region_id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "North America",
        "requires_physical_presence": True,
        "allows_remote_work": True
    }
)
```

### Running the Example

The `example.py` file contains a complete workflow example that demonstrates the main features of the service. To run it:

```python
from opportunity_management_service.example import run_example

run_example()
```

### Running Tests

The `tests.py` file contains unit tests for the implementation. To run the tests:

```python
import unittest
from opportunity_management_service.tests import TestUser, TestOpportunity, TestProblemStatement, TestOpportunityService

if __name__ == '__main__':
    unittest.main()
```

## Business Rules

The implementation enforces the following key business rules:

1. **Opportunity Creation**:
   - Required fields must be provided (customer name, title, description, start date, end date, priority, ARR)
   - Initial status is "Draft"

2. **Problem Statement**:
   - Minimum character count of 140 characters
   - Rich text formatting support

3. **Skills Requirements**:
   - At least one skill must be specified
   - At least one "Must Have" skill is required
   - Skills must come from the Skills Catalog

4. **Timeline**:
   - End date must be after start date
   - Specific days must fall within the start and end dates

5. **Status Transitions**:
   - Status changes must follow the defined workflow
   - Status changes are tracked with timestamp and user

6. **Opportunity Modification**:
   - No modifications allowed after a Solution Architect is selected
   - All modifications are recorded in change history

7. **Opportunity Cancellation**:
   - Cancellation requires a reason
   - Cancelled opportunities can be reactivated within 90 days

## Event System

The implementation includes a simple event system for notifications:

- `opportunity.created`: Published when a new opportunity is created
- `opportunity.submitted`: Published when an opportunity is submitted for matching
- `opportunity.cancelled`: Published when an opportunity is cancelled
- `opportunity.reactivated`: Published when a cancelled opportunity is reactivated

## Extending the Implementation

To extend this implementation:

1. **Persistent Storage**: Replace the in-memory repositories with implementations that use a database
2. **API Layer**: Add REST or GraphQL API endpoints to expose the service
3. **Authentication**: Integrate with an authentication system
4. **Advanced Validation**: Add more sophisticated validation rules
5. **UI Integration**: Connect the service to a user interface
