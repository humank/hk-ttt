# Step 7: Adapt Service Layer

This document outlines the necessary adaptations to the service layer to work with the API layer for the Opportunity Management Service.

## Service Layer Adaptations

Our existing service layer was designed with a domain-driven approach, but we need to make some adaptations to ensure it works seamlessly with the API layer:

1. Dependency injection for repositories
2. Transaction management
3. Asynchronous operations
4. Integration with authentication and authorization
5. Error handling and exceptions
6. Logging and monitoring

## Dependency Injection for Repositories

We'll use FastAPI's dependency injection system to provide repositories to our service layer:

```python
from fastapi import Depends
from typing import Annotated

# Repository interfaces
class OpportunityRepository(Protocol):
    async def create(self, opportunity: Opportunity) -> Opportunity: ...
    async def get_by_id(self, opportunity_id: str) -> Optional[Opportunity]: ...
    async def update(self, opportunity: Opportunity) -> Opportunity: ...
    async def delete(self, opportunity_id: str) -> bool: ...
    async def list(self, filters: dict, page: int, size: int) -> Tuple[List[Opportunity], int]: ...

# Repository implementations
class PostgresOpportunityRepository(OpportunityRepository):
    def __init__(self, db_pool):
        self.db_pool = db_pool
    
    async def create(self, opportunity: Opportunity) -> Opportunity:
        async with self.db_pool.acquire() as conn:
            # Implementation
            pass
    
    # Other methods...

# Repository providers
async def get_opportunity_repository(
    db_pool = Depends(get_db_pool)
) -> OpportunityRepository:
    return PostgresOpportunityRepository(db_pool)

# Service with dependency injection
class OpportunityService:
    def __init__(
        self, 
        opportunity_repo: OpportunityRepository,
        problem_statement_repo: ProblemStatementRepository,
        skill_requirement_repo: SkillRequirementRepository,
        timeline_requirement_repo: TimelineRequirementRepository,
        attachment_repo: AttachmentRepository,
        change_record_repo: ChangeRecordRepository
    ):
        self.opportunity_repo = opportunity_repo
        self.problem_statement_repo = problem_statement_repo
        self.skill_requirement_repo = skill_requirement_repo
        self.timeline_requirement_repo = timeline_requirement_repo
        self.attachment_repo = attachment_repo
        self.change_record_repo = change_record_repo

# Service provider
async def get_opportunity_service(
    opportunity_repo: OpportunityRepository = Depends(get_opportunity_repository),
    problem_statement_repo: ProblemStatementRepository = Depends(get_problem_statement_repository),
    skill_requirement_repo: SkillRequirementRepository = Depends(get_skill_requirement_repository),
    timeline_requirement_repo: TimelineRequirementRepository = Depends(get_timeline_requirement_repository),
    attachment_repo: AttachmentRepository = Depends(get_attachment_repository),
    change_record_repo: ChangeRecordRepository = Depends(get_change_record_repository)
) -> OpportunityService:
    return OpportunityService(
        opportunity_repo,
        problem_statement_repo,
        skill_requirement_repo,
        timeline_requirement_repo,
        attachment_repo,
        change_record_repo
    )

# Usage in API route
@app.post("/api/v1/opportunities", response_model=OpportunityResponse)
async def create_opportunity(
    request: OpportunityCreateRequest,
    opportunity_service: OpportunityService = Depends(get_opportunity_service),
    current_user: User = Depends(get_current_user)
):
    # Implementation
    pass
```

## Transaction Management

We'll implement a transaction manager to ensure database operations are atomic:

```python
from contextlib import asynccontextmanager

class TransactionManager:
    def __init__(self, db_pool):
        self.db_pool = db_pool
    
    @asynccontextmanager
    async def transaction(self):
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                yield conn

# Repository with transaction support
class PostgresOpportunityRepository(OpportunityRepository):
    def __init__(self, db_pool, transaction_manager=None):
        self.db_pool = db_pool
        self.transaction_manager = transaction_manager or TransactionManager(db_pool)
    
    async def create(self, opportunity: Opportunity, conn=None) -> Opportunity:
        if conn:
            # Use provided connection (within transaction)
            return await self._create(opportunity, conn)
        else:
            # Create own connection
            async with self.db_pool.acquire() as conn:
                return await self._create(opportunity, conn)
    
    async def _create(self, opportunity: Opportunity, conn) -> Opportunity:
        # Implementation using the provided connection
        pass

# Service with transaction support
class OpportunityService:
    def __init__(
        self, 
        opportunity_repo: OpportunityRepository,
        problem_statement_repo: ProblemStatementRepository,
        # Other repositories...
        transaction_manager: TransactionManager
    ):
        self.opportunity_repo = opportunity_repo
        self.problem_statement_repo = problem_statement_repo
        # Other repositories...
        self.transaction_manager = transaction_manager
    
    async def create_opportunity_with_components(
        self, 
        opportunity: Opportunity,
        problem_statements: List[ProblemStatement],
        skill_requirements: List[SkillRequirement],
        timeline_requirements: List[TimelineRequirement],
        user: User
    ) -> Opportunity:
        async with self.transaction_manager.transaction() as conn:
            # Create opportunity
            created_opportunity = await self.opportunity_repo.create(opportunity, conn)
            
            # Create problem statements
            for statement in problem_statements:
                statement.opportunity_id = created_opportunity.id
                await self.problem_statement_repo.create(statement, conn)
            
            # Create skill requirements
            for requirement in skill_requirements:
                requirement.opportunity_id = created_opportunity.id
                await self.skill_requirement_repo.create(requirement, conn)
            
            # Create timeline requirements
            for requirement in timeline_requirements:
                requirement.opportunity_id = created_opportunity.id
                await self.timeline_requirement_repo.create(requirement, conn)
            
            return created_opportunity
```

## Asynchronous Operations

We'll adapt our service layer to use asynchronous operations for better performance:

```python
class OpportunityService:
    async def create_opportunity(self, opportunity: Opportunity, user: User) -> Opportunity:
        # Validate opportunity
        self._validate_opportunity(opportunity)
        
        # Check authorization
        if not self._can_create_opportunity(user):
            raise AuthorizationError("User does not have permission to create opportunities")
        
        # Set created_by
        opportunity.created_by = user.id
        
        # Create opportunity
        created_opportunity = await self.opportunity_repo.create(opportunity)
        
        # Create change record
        change_record = ChangeRecord(
            id=str(uuid.uuid4()),
            entity_id=created_opportunity.id,
            entity_type="Opportunity",
            field_name="status",
            old_value=None,
            new_value=created_opportunity.status.value,
            changed_at=datetime.now(),
            changed_by=user.id
        )
        await self.change_record_repo.create(change_record)
        
        return created_opportunity
    
    async def get_opportunity(self, opportunity_id: str, user: User) -> Optional[Opportunity]:
        opportunity = await self.opportunity_repo.get_by_id(opportunity_id)
        
        if not opportunity:
            return None
        
        if not self._can_view_opportunity(opportunity, user):
            raise AuthorizationError("User does not have permission to view this opportunity")
        
        # Load related entities
        opportunity.problem_statements = await self.problem_statement_repo.get_by_opportunity_id(opportunity_id)
        opportunity.skill_requirements = await self.skill_requirement_repo.get_by_opportunity_id(opportunity_id)
        opportunity.timeline_requirements = await self.timeline_requirement_repo.get_by_opportunity_id(opportunity_id)
        opportunity.attachments = await self.attachment_repo.get_by_opportunity_id(opportunity_id)
        opportunity.change_history = await self.change_record_repo.get_by_entity_id(opportunity_id)
        
        return opportunity
```

## Integration with Authentication and Authorization

We'll integrate our service layer with the authentication and authorization system:

```python
class OpportunityService:
    def _can_create_opportunity(self, user: User) -> bool:
        return user.role in [Role.ADMIN, Role.SALES_MANAGER]
    
    def _can_view_opportunity(self, opportunity: Opportunity, user: User) -> bool:
        # Admins and sales managers can view all opportunities
        if user.role in [Role.ADMIN, Role.SALES_MANAGER]:
            return True
        
        # Sales representatives can only view their own opportunities
        if user.role == Role.SALES_REPRESENTATIVE:
            return opportunity.created_by == user.id
        
        return False
    
    def _can_update_opportunity(self, opportunity: Opportunity, user: User) -> bool:
        # Admins can update all opportunities
        if user.role == Role.ADMIN:
            return True
        
        # Sales managers can update all opportunities
        if user.role == Role.SALES_MANAGER:
            return True
        
        # Sales representatives can only update their own opportunities in DRAFT status
        if user.role == Role.SALES_REPRESENTATIVE:
            return opportunity.created_by == user.id and opportunity.status == OpportunityStatus.DRAFT
        
        return False
    
    def _can_change_status(self, opportunity: Opportunity, new_status: OpportunityStatus, user: User) -> bool:
        # Admins can change any status
        if user.role == Role.ADMIN:
            return True
        
        # Sales managers can change any status
        if user.role == Role.SALES_MANAGER:
            return True
        
        # Sales representatives can only change status from DRAFT to SUBMITTED
        if user.role == Role.SALES_REPRESENTATIVE:
            return (
                opportunity.created_by == user.id and
                opportunity.status == OpportunityStatus.DRAFT and
                new_status == OpportunityStatus.SUBMITTED
            )
        
        return False
```

## Error Handling and Exceptions

We'll define a set of custom exceptions for our service layer:

```python
class ServiceError(Exception):
    """Base class for service exceptions"""
    pass

class ValidationError(ServiceError):
    """Raised when validation fails"""
    pass

class AuthorizationError(ServiceError):
    """Raised when authorization fails"""
    pass

class ResourceNotFoundError(ServiceError):
    """Raised when a resource is not found"""
    pass

class BusinessRuleViolationError(ServiceError):
    """Raised when a business rule is violated"""
    pass

# Usage in service
class OpportunityService:
    def _validate_opportunity(self, opportunity: Opportunity):
        errors = []
        
        if not opportunity.title:
            errors.append("Title is required")
        
        if not opportunity.description:
            errors.append("Description is required")
        
        if not opportunity.client_name:
            errors.append("Client name is required")
        
        if opportunity.estimated_budget is None or opportunity.estimated_budget <= 0:
            errors.append("Estimated budget must be greater than zero")
        
        if opportunity.estimated_start_date and opportunity.estimated_end_date:
            if opportunity.estimated_start_date > opportunity.estimated_end_date:
                errors.append("Estimated start date must be before estimated end date")
        
        if errors:
            raise ValidationError(", ".join(errors))
```

## Logging and Monitoring

We'll add logging and monitoring to our service layer:

```python
import logging
import time
from contextlib import contextmanager

logger = logging.getLogger(__name__)

@contextmanager
def log_execution_time(operation_name):
    start_time = time.time()
    try:
        yield
    finally:
        execution_time = time.time() - start_time
        logger.info(f"{operation_name} completed in {execution_time:.2f}s")

class OpportunityService:
    async def create_opportunity(self, opportunity: Opportunity, user: User) -> Opportunity:
        with log_execution_time("create_opportunity"):
            logger.info(f"Creating opportunity with title: {opportunity.title}")
            
            try:
                # Validate opportunity
                self._validate_opportunity(opportunity)
                
                # Check authorization
                if not self._can_create_opportunity(user):
                    logger.warning(f"User {user.id} attempted to create opportunity without permission")
                    raise AuthorizationError("User does not have permission to create opportunities")
                
                # Set created_by
                opportunity.created_by = user.id
                
                # Create opportunity
                created_opportunity = await self.opportunity_repo.create(opportunity)
                
                # Create change record
                change_record = ChangeRecord(
                    id=str(uuid.uuid4()),
                    entity_id=created_opportunity.id,
                    entity_type="Opportunity",
                    field_name="status",
                    old_value=None,
                    new_value=created_opportunity.status.value,
                    changed_at=datetime.now(),
                    changed_by=user.id
                )
                await self.change_record_repo.create(change_record)
                
                logger.info(f"Created opportunity with ID: {created_opportunity.id}")
                return created_opportunity
            except Exception as e:
                logger.error(f"Error creating opportunity: {str(e)}", exc_info=True)
                raise
```

## Caching Integration

We'll integrate our service layer with the caching system:

```python
from functools import wraps
import json
import hashlib

class CacheService:
    def __init__(self, redis_client):
        self.redis_client = redis_client
    
    async def get(self, key: str) -> Optional[str]:
        return await self.redis_client.get(key)
    
    async def set(self, key: str, value: str, ttl_seconds: int = 300) -> bool:
        return await self.redis_client.set(key, value, ex=ttl_seconds)
    
    async def delete(self, key: str) -> bool:
        return await self.redis_client.delete(key)
    
    async def delete_pattern(self, pattern: str) -> int:
        keys = await self.redis_client.keys(pattern)
        if keys:
            return await self.redis_client.delete(*keys)
        return 0

def cached(ttl_seconds=300, prefix="cache"):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            # Generate cache key
            key_parts = [prefix, func.__name__]
            
            # Add args to key
            for arg in args:
                if hasattr(arg, "id"):
                    key_parts.append(str(arg.id))
                else:
                    key_parts.append(str(arg))
            
            # Add kwargs to key
            for k, v in sorted(kwargs.items()):
                if k == "user":  # Skip user for caching
                    continue
                if hasattr(v, "id"):
                    key_parts.append(f"{k}:{v.id}")
                else:
                    key_parts.append(f"{k}:{v}")
            
            cache_key = ":".join(key_parts)
            
            # Try to get from cache
            cached_value = await self.cache_service.get(cache_key)
            if cached_value:
                try:
                    return json.loads(cached_value)
                except json.JSONDecodeError:
                    pass
            
            # Execute function
            result = await func(self, *args, **kwargs)
            
            # Store in cache
            if result is not None:
                try:
                    await self.cache_service.set(
                        cache_key,
                        json.dumps(result),
                        ttl_seconds
                    )
                except (TypeError, json.JSONEncodeError):
                    pass
            
            return result
        return wrapper
    return decorator

# Usage in service
class OpportunityService:
    def __init__(
        self, 
        opportunity_repo: OpportunityRepository,
        # Other repositories...
        cache_service: CacheService
    ):
        self.opportunity_repo = opportunity_repo
        # Other repositories...
        self.cache_service = cache_service
    
    @cached(ttl_seconds=300, prefix="opportunity")
    async def get_opportunity(self, opportunity_id: str, user: User) -> Optional[Opportunity]:
        # Implementation
        pass
    
    async def update_opportunity(self, opportunity: Opportunity, user: User) -> Opportunity:
        # Implementation
        
        # Invalidate cache
        await self.cache_service.delete(f"opportunity:get_opportunity:{opportunity.id}")
        await self.cache_service.delete_pattern(f"opportunity:list_opportunities:*")
        
        return updated_opportunity
```

## Service Layer Adapters

We'll create adapter classes to convert between API models and domain models:

```python
class OpportunityAdapter:
    @staticmethod
    def to_domain(request: OpportunityCreateRequest) -> Opportunity:
        return Opportunity(
            id=str(uuid.uuid4()),
            title=request.title,
            description=request.description,
            client_name=request.client_name,
            estimated_budget=request.estimated_budget,
            estimated_start_date=request.estimated_start_date,
            estimated_end_date=request.estimated_end_date,
            status=OpportunityStatus(request.status),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by=None,  # Will be set by service
            problem_statements=[],
            skill_requirements=[],
            timeline_requirements=[],
            attachments=[],
            change_history=[]
        )
    
    @staticmethod
    def to_response(opportunity: Opportunity) -> OpportunityResponse:
        return OpportunityResponse(
            id=opportunity.id,
            title=opportunity.title,
            description=opportunity.description,
            client_name=opportunity.client_name,
            estimated_budget=opportunity.estimated_budget,
            estimated_start_date=opportunity.estimated_start_date,
            estimated_end_date=opportunity.estimated_end_date,
            status=opportunity.status.value,
            created_at=opportunity.created_at,
            updated_at=opportunity.updated_at,
            created_by=opportunity.created_by,
            problem_statements=[
                ProblemStatementAdapter.to_response(ps)
                for ps in opportunity.problem_statements
            ],
            skill_requirements=[
                SkillRequirementAdapter.to_response(sr)
                for sr in opportunity.skill_requirements
            ],
            timeline_requirements=[
                TimelineRequirementAdapter.to_response(tr)
                for tr in opportunity.timeline_requirements
            ],
            attachments=[
                AttachmentAdapter.to_response(a)
                for a in opportunity.attachments
            ],
            change_history=[
                ChangeRecordAdapter.to_response(cr)
                for cr in opportunity.change_history
            ]
        )
```

## API Route Implementation

Finally, we'll implement the API routes using our adapted service layer:

```python
@app.post("/api/v1/opportunities", response_model=OpportunityResponse, status_code=201)
async def create_opportunity(
    request: OpportunityCreateRequest,
    opportunity_service: OpportunityService = Depends(get_opportunity_service),
    current_user: User = Depends(has_role([Role.ADMIN, Role.SALES_MANAGER]))
):
    try:
        # Convert request to domain model
        opportunity = OpportunityAdapter.to_domain(request)
        
        # Call service layer
        created_opportunity = await opportunity_service.create_opportunity(opportunity, current_user)
        
        # Convert domain model to response
        return OpportunityAdapter.to_response(created_opportunity)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AuthorizationError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating opportunity: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/opportunities/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(
    opportunity_id: str,
    opportunity_service: OpportunityService = Depends(get_opportunity_service),
    current_user: User = Depends(get_current_user)
):
    try:
        opportunity = await opportunity_service.get_opportunity(opportunity_id, current_user)
        
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        
        return OpportunityAdapter.to_response(opportunity)
    except AuthorizationError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting opportunity: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
```

## Next Steps

1. Implement the repository adapters for PostgreSQL
2. Implement the caching service
3. Implement the transaction manager
4. Update the service layer with asynchronous operations
5. Integrate with authentication and authorization
6. Add logging and monitoring
7. Implement the API routes
