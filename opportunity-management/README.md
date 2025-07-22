# Opportunity Management System - Domain Model Implementation

A comprehensive Python implementation of the Opportunity Management Service domain model, designed using Domain-Driven Design (DDD) principles with clean architecture patterns.

## Overview

This implementation provides a complete domain model for managing customer opportunities in a solution architecture consulting context. It supports the full lifecycle from opportunity creation through completion, with comprehensive business rule enforcement and event-driven architecture.

## Features

### Core Functionality
- **Opportunity Lifecycle Management**: Complete CRUD operations with status transitions
- **Skills Requirements Management**: Comprehensive skill specification with importance levels
- **Timeline Management**: Flexible timeline specification and validation
- **Problem Statement Documentation**: Rich content management with attachments
- **Status Tracking**: Real-time status updates with history tracking
- **Business Rule Enforcement**: Comprehensive validation and constraint checking

### Advanced Features
- **Event-Driven Architecture**: Domain events with configurable handlers
- **Opportunity Cloning**: Template-based opportunity creation
- **Cancellation & Reactivation**: 90-day reactivation window
- **Dashboard & Reporting**: Sales manager dashboard with analytics
- **Matching Preparation**: Criteria preparation for architect matching
- **Audit Trail**: Complete change history and versioning

### Technical Features
- **Domain-Driven Design**: Clean separation of concerns
- **In-Memory Repositories**: Simple dictionary-based storage
- **Comprehensive Validation**: Multi-layer validation with custom exceptions
- **Type Hints**: Full type annotation throughout
- **Logging Integration**: Structured logging with Python's logging module
- **Pydantic Models**: Data validation and serialization
- **Simple Dependency Injection**: Service composition patterns

## Architecture

### Domain Model Structure

```
Domain Layer
├── Entities
│   ├── Opportunity (Aggregate Root)
│   ├── Customer
│   ├── ProblemStatement
│   └── StatusHistory
├── Value Objects
│   ├── SkillRequirement
│   ├── TimelineSpecification
│   ├── GeographicRequirement
│   ├── LanguageRequirement
│   └── DocumentAttachment
├── Enumerations
│   ├── Priority
│   ├── OpportunityStatus
│   ├── SkillImportance
│   └── TimelineFlexibility
└── Domain Events
    ├── OpportunityCreatedEvent
    ├── OpportunityModifiedEvent
    ├── OpportunityCancelledEvent
    └── StatusChangedEvent

Application Layer
├── Application Services
│   ├── OpportunityApplicationService
│   └── OpportunityQueryService
└── Domain Services
    ├── OpportunityValidationService
    ├── StatusTransitionService
    ├── OpportunityModificationService
    └── SkillsMatchingPreparationService

Infrastructure Layer
├── Repositories
│   ├── InMemoryOpportunityRepository
│   └── InMemoryCustomerRepository
├── Event Handling
│   └── EventDispatcher
└── Utilities
    ├── Validators
    ├── DateUtils
    └── Custom Exceptions
```

## User Stories Implemented

The implementation covers all specified user stories:

- **US-SM-3**: Customer Opportunity Creation
- **US-SM-4**: Problem Statement Documentation
- **US-SM-5**: Required Skills Specification
- **US-SM-6**: Opportunity Timeline Management
- **US-SM-7**: Opportunity Status Tracking
- **US-SM-8**: Opportunity Modification
- **US-SM-9**: Opportunity Cancellation

## Quick Start

### Basic Usage Example

```python
from example_usage import main

# Run the complete demonstration
main()
```

### Creating an Opportunity

```python
from opportunity_application_service import OpportunityApplicationService
from in_memory_opportunity_repository import InMemoryOpportunityRepository
from in_memory_customer_repository import InMemoryCustomerRepository
# ... other imports

# Setup services
opportunity_repo = InMemoryOpportunityRepository()
customer_repo = InMemoryCustomerRepository()
# ... setup other services

app_service = OpportunityApplicationService(
    opportunity_repo, customer_repo, validation_service,
    status_transition_service, modification_service, matching_preparation_service
)

# Create opportunity
opportunity_data = {
    "title": "Cloud Migration Project",
    "description": "Migrate legacy systems to AWS",
    "customer_name": "Acme Corp",  # Will create customer if not exists
    "sales_manager_id": "sm_001",
    "annual_recurring_revenue": "750000",
    "priority": "High"
}

result = app_service.create_opportunity(opportunity_data)
if result["success"]:
    opportunity_id = result["opportunity_id"]
    print(f"Opportunity created: {opportunity_id}")
```

### Adding Skills Requirements

```python
skills_data = [
    {
        "skill_name": "AWS",
        "skill_category": "Technical",
        "importance": "Must Have",
        "proficiency_level": "Advanced",
        "description": "AWS cloud services expertise"
    },
    {
        "skill_name": "Communication",
        "skill_category": "Soft",
        "importance": "Must Have",
        "description": "Excellent client communication skills"
    }
]

result = app_service.add_skill_requirements(opportunity_id, skills_data, "sm_001")
```

### Status Transitions

```python
# Submit for matching
result = app_service.submit_opportunity(opportunity_id, "sm_001")

# Cancel opportunity
result = app_service.cancel_opportunity(
    opportunity_id, "Budget constraints", "sm_001"
)

# Reactivate within 90 days
result = app_service.reactivate_opportunity(opportunity_id, "sm_001")
```

## Testing

### Running Tests

```bash
# Run individual test modules
python test_opportunity_creation.py
python test_status_transitions.py
python test_skills_management.py

# Run comprehensive example
python example_usage.py
```

### Test Coverage

The implementation includes comprehensive tests for:

- **Opportunity Creation Workflow**: End-to-end opportunity creation
- **Status Transitions**: All valid and invalid status changes
- **Skills Management**: Skills validation, modification, and matching preparation
- **Validation Scenarios**: Edge cases and error conditions
- **Event System**: Domain event handling and dispatching

## Configuration

### Event Handling

```python
from event_dispatcher import get_event_dispatcher

# Get global event dispatcher
dispatcher = get_event_dispatcher()

# Register custom event handler
def handle_opportunity_created(event):
    print(f"New opportunity: {event.opportunity_title}")

dispatcher.register_function_handler("OpportunityCreatedEvent", handle_opportunity_created)
```

### Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Business Rules

### Opportunity Status Transitions

```
Draft → Submitted → Matching in Progress → Matches Found → Architect Selected → Completed
  ↓                                                                              ↑
Cancelled ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
  ↓
Draft (Reactivation within 90 days)
```

### Modification Rules

- **Draft/Submitted**: Full modification allowed
- **Architect Selected**: Limited modifications (priority, notes only)
- **Completed/Cancelled**: No modifications allowed

### Validation Rules

- **Opportunity Creation**: Title, description, customer, sales manager, positive ARR required
- **Skills Requirements**: At least one mandatory skill required
- **Timeline**: Start date cannot be in past, duration must be positive
- **Problem Statement**: Minimum 50 characters for description

## Data Models

### Opportunity Entity

```python
@dataclass
class Opportunity(AggregateRoot):
    title: str
    description: str
    customer_id: str
    sales_manager_id: str
    annual_recurring_revenue: Decimal
    priority: Priority
    status: OpportunityStatus = OpportunityStatus.DRAFT
    # ... additional fields
```

### Skill Requirement Value Object

```python
@dataclass(frozen=True)
class SkillRequirement:
    skill_name: str
    skill_category: str  # Technical, Soft, Industry
    importance: SkillImportance
    proficiency_level: Optional[str] = None
    description: Optional[str] = None
```

## Error Handling

The system includes comprehensive custom exceptions:

- `ValidationException`: Validation failures
- `OpportunityNotFoundException`: Entity not found
- `InvalidStatusTransitionException`: Invalid status changes
- `BusinessRuleViolationException`: Business rule violations
- `ReactivationNotAllowedException`: Invalid reactivation attempts

## Performance Considerations

### In-Memory Storage

- Suitable for development and testing
- Easy to replace with persistent storage
- Dictionary-based lookups for O(1) access
- No external dependencies

### Scalability

- Repository pattern allows easy database integration
- Event-driven architecture supports distributed systems
- Service layer enables horizontal scaling
- Stateless design for cloud deployment

## Extension Points

### Custom Repositories

```python
class DatabaseOpportunityRepository(OpportunityRepository):
    def save(self, opportunity: Opportunity) -> Opportunity:
        # Implement database persistence
        pass
```

### Custom Event Handlers

```python
class EmailNotificationHandler(EventHandler):
    def handle(self, event: DomainEvent) -> None:
        # Send email notifications
        pass
```

### Additional Validation

```python
class CustomValidationService(OpportunityValidationService):
    def validate_for_creation(self, data: Dict[str, Any]) -> List[str]:
        errors = super().validate_for_creation(data)
        # Add custom validation logic
        return errors
```

## Dependencies

### Required Python Packages

```
python >= 3.8
dataclasses (built-in)
datetime (built-in)
decimal (built-in)
typing (built-in)
uuid (built-in)
logging (built-in)
re (built-in)
```

### Optional Dependencies

```
pydantic  # For enhanced data validation
```

## Contributing

### Code Style

- Follow PEP 8 guidelines
- Use type hints throughout
- Include comprehensive docstrings
- Write meaningful variable names
- Keep functions focused and small

### Testing

- Write tests for new features
- Include edge case testing
- Maintain test coverage
- Use descriptive test names

## License

This implementation is provided as an educational example of Domain-Driven Design patterns in Python.

## Support

For questions or issues with this implementation, please refer to the comprehensive test examples and documentation provided in the codebase.

---

**Note**: This is a domain model implementation focused on demonstrating DDD principles. For production use, consider adding persistent storage, authentication, authorization, API layers, and comprehensive error handling.
