"""
In-memory repository implementations for the Opportunity Management Service.
"""

import uuid
from typing import Dict, List, Optional, TypeVar, Generic, Any
from datetime import datetime
import logging
import re

from .common import NotFoundException
from .repositories import (
    UserRepository, CustomerRepository, SkillsCatalogRepository,
    OpportunityRepository, ProblemStatementRepository, SkillRequirementRepository,
    TimelineRequirementRepository, OpportunityStatusRepository,
    AttachmentRepository, ChangeRecordRepository
)
from .user import User
from .customer import Customer
from .skills_catalog import SkillsCatalog
from .opportunity import Opportunity
from .problem_statement import ProblemStatement
from .skill_requirement import SkillRequirement
from .timeline_requirement import TimelineRequirement
from .opportunity_status import OpportunityStatus
from .attachment import Attachment
from .change_record import ChangeRecord
from .enums import UserRole

logger = logging.getLogger(__name__)

T = TypeVar('T')

class InMemoryRepository(Generic[T]):
    """Base in-memory repository implementation."""
    
    def __init__(self):
        self._entities: Dict[uuid.UUID, T] = {}
    
    def add(self, entity: T) -> T:
        """Add an entity to the repository."""
        self._entities[entity.id] = entity
        logger.info(f"Added entity with ID {entity.id} to repository")
        return entity
    
    def get_by_id(self, entity_id: uuid.UUID) -> Optional[T]:
        """Get an entity by its ID."""
        entity = self._entities.get(entity_id)
        if not entity:
            logger.warning(f"Entity with ID {entity_id} not found")
            return None
        return entity
    
    def update(self, entity: T) -> T:
        """Update an entity in the repository."""
        if entity.id not in self._entities:
            raise NotFoundException(f"Entity with ID {entity.id} not found")
        
        self._entities[entity.id] = entity
        logger.info(f"Updated entity with ID {entity.id}")
        return entity
    
    def remove(self, entity_id: uuid.UUID) -> bool:
        """Remove an entity from the repository."""
        if entity_id not in self._entities:
            logger.warning(f"Entity with ID {entity_id} not found for removal")
            return False
        
        del self._entities[entity_id]
        logger.info(f"Removed entity with ID {entity_id}")
        return True
    
    def get_all(self) -> List[T]:
        """Get all entities from the repository."""
        return list(self._entities.values())

class InMemoryUserRepository(InMemoryRepository[User], UserRepository):
    """In-memory implementation of UserRepository."""
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        for user in self._entities.values():
            if user.email == email:
                return user
        return None
    
    def get_by_employee_id(self, employee_id: str) -> Optional[User]:
        """Get a user by employee ID."""
        for user in self._entities.values():
            if user.employee_id == employee_id:
                return user
        return None
    
    def get_sales_managers(self) -> List[User]:
        """Get all sales managers."""
        return [user for user in self._entities.values() 
                if user.role == UserRole.SALES_MANAGER and user.is_active]
    
    def get_solution_architects(self) -> List[User]:
        """Get all solution architects."""
        return [user for user in self._entities.values() 
                if user.role == UserRole.SOLUTION_ARCHITECT and user.is_active]

class InMemoryCustomerRepository(InMemoryRepository[Customer], CustomerRepository):
    """In-memory implementation of CustomerRepository."""
    
    def get_by_name(self, name: str) -> List[Customer]:
        """Get customers by name (partial match)."""
        return [customer for customer in self._entities.values() 
                if name.lower() in customer.name.lower()]
    
    def get_active_customers(self) -> List[Customer]:
        """Get all active customers."""
        return [customer for customer in self._entities.values() if customer.is_active]

class InMemorySkillsCatalogRepository(InMemoryRepository[SkillsCatalog], SkillsCatalogRepository):
    """In-memory implementation of SkillsCatalogRepository."""
    
    def get_by_name(self, name: str) -> List[SkillsCatalog]:
        """Get skills by name (partial match)."""
        return [skill for skill in self._entities.values() 
                if name.lower() in skill.name.lower()]
    
    def get_by_category(self, category: str) -> List[SkillsCatalog]:
        """Get skills by category."""
        return [skill for skill in self._entities.values() 
                if skill.category.value == category]
    
    def get_active_skills(self) -> List[SkillsCatalog]:
        """Get all active skills."""
        return [skill for skill in self._entities.values() if skill.is_active]
    
    def search_skills(self, query: str) -> List[SkillsCatalog]:
        """Search skills by name, category, or description."""
        query = query.lower()
        return [skill for skill in self._entities.values() 
                if (query in skill.name.lower() or 
                    query in skill.description.lower() or 
                    query in skill.category.value.lower() or
                    (skill.subcategory and query in skill.subcategory.lower()) or
                    any(query in synonym.lower() for synonym in skill.synonyms))]

class InMemoryOpportunityRepository(InMemoryRepository[Opportunity], OpportunityRepository):
    """In-memory implementation of OpportunityRepository."""
    
    def get_by_sales_manager(self, sales_manager_id: uuid.UUID) -> List[Opportunity]:
        """Get opportunities by sales manager."""
        return [opportunity for opportunity in self._entities.values() 
                if opportunity.sales_manager_id == sales_manager_id]
    
    def get_by_customer(self, customer_id: uuid.UUID) -> List[Opportunity]:
        """Get opportunities by customer."""
        return [opportunity for opportunity in self._entities.values() 
                if opportunity.customer_id == customer_id]
    
    def get_by_status(self, status: str) -> List[Opportunity]:
        """Get opportunities by status."""
        return [opportunity for opportunity in self._entities.values() 
                if opportunity.status.value == status]
    
    def get_by_priority(self, priority: str) -> List[Opportunity]:
        """Get opportunities by priority."""
        return [opportunity for opportunity in self._entities.values() 
                if opportunity.priority.value == priority]
    
    def search_opportunities(self, query: str) -> List[Opportunity]:
        """Search opportunities by title or description."""
        query = query.lower()
        return [opportunity for opportunity in self._entities.values() 
                if query in opportunity.title.lower() or query in opportunity.description.lower()]

class InMemoryProblemStatementRepository(InMemoryRepository[ProblemStatement], ProblemStatementRepository):
    """In-memory implementation of ProblemStatementRepository."""
    
    def get_by_opportunity(self, opportunity_id: uuid.UUID) -> Optional[ProblemStatement]:
        """Get problem statement by opportunity."""
        for statement in self._entities.values():
            if statement.opportunity_id == opportunity_id:
                return statement
        return None
    
    def search_problem_statements(self, query: str) -> List[ProblemStatement]:
        """Search problem statements by content."""
        query = query.lower()
        return [statement for statement in self._entities.values() 
                if query in statement.content.lower()]

class InMemorySkillRequirementRepository(InMemoryRepository[SkillRequirement], SkillRequirementRepository):
    """In-memory implementation of SkillRequirementRepository."""
    
    def get_by_opportunity(self, opportunity_id: uuid.UUID) -> List[SkillRequirement]:
        """Get skill requirements by opportunity."""
        return [requirement for requirement in self._entities.values() 
                if requirement.opportunity_id == opportunity_id]
    
    def get_by_skill(self, skill_id: uuid.UUID) -> List[SkillRequirement]:
        """Get skill requirements by skill."""
        return [requirement for requirement in self._entities.values() 
                if requirement.skill_id == skill_id]
    
    def get_must_have_skills(self, opportunity_id: uuid.UUID) -> List[SkillRequirement]:
        """Get 'Must Have' skill requirements for an opportunity."""
        return [requirement for requirement in self._entities.values() 
                if requirement.opportunity_id == opportunity_id and 
                requirement.importance_level.value == "Must Have"]

class InMemoryTimelineRequirementRepository(InMemoryRepository[TimelineRequirement], TimelineRequirementRepository):
    """In-memory implementation of TimelineRequirementRepository."""
    
    def get_by_opportunity(self, opportunity_id: uuid.UUID) -> Optional[TimelineRequirement]:
        """Get timeline requirement by opportunity."""
        for timeline in self._entities.values():
            if timeline.opportunity_id == opportunity_id:
                return timeline
        return None
    
    def get_by_date_range(self, start_date: str, end_date: str) -> List[TimelineRequirement]:
        """Get timeline requirements within a date range."""
        from dateutil.parser import parse
        
        start = parse(start_date).date()
        end = parse(end_date).date()
        
        result = []
        for timeline in self._entities.values():
            timeline_start = parse(timeline.expected_start_date).date()
            timeline_end = parse(timeline.expected_end_date).date()
            
            # Check if there's any overlap between the date ranges
            if (timeline_start <= end and timeline_end >= start):
                result.append(timeline)
        
        return result

class InMemoryOpportunityStatusRepository(InMemoryRepository[OpportunityStatus], OpportunityStatusRepository):
    """In-memory implementation of OpportunityStatusRepository."""
    
    def get_by_opportunity(self, opportunity_id: uuid.UUID) -> List[OpportunityStatus]:
        """Get status records by opportunity."""
        return [status for status in self._entities.values() 
                if status.opportunity_id == opportunity_id]
    
    def get_current_status(self, opportunity_id: uuid.UUID) -> Optional[OpportunityStatus]:
        """Get the current status record for an opportunity."""
        statuses = self.get_by_opportunity(opportunity_id)
        if not statuses:
            return None
        
        # Return the most recent status
        return max(statuses, key=lambda s: s.changed_at)
    
    def get_status_history(self, opportunity_id: uuid.UUID) -> List[OpportunityStatus]:
        """Get the complete status history for an opportunity."""
        statuses = self.get_by_opportunity(opportunity_id)
        # Sort by changed_at timestamp
        return sorted(statuses, key=lambda s: s.changed_at)

class InMemoryAttachmentRepository(InMemoryRepository[Attachment], AttachmentRepository):
    """In-memory implementation of AttachmentRepository."""
    
    def get_by_problem_statement(self, problem_statement_id: uuid.UUID) -> List[Attachment]:
        """Get attachments by problem statement."""
        return [attachment for attachment in self._entities.values() 
                if attachment.problem_statement_id == problem_statement_id]
    
    def get_by_file_type(self, file_type: str) -> List[Attachment]:
        """Get attachments by file type."""
        return [attachment for attachment in self._entities.values() 
                if attachment.file_type == file_type]
    
    def get_active_attachments(self, problem_statement_id: uuid.UUID) -> List[Attachment]:
        """Get active (not removed) attachments for a problem statement."""
        return [attachment for attachment in self._entities.values() 
                if attachment.problem_statement_id == problem_statement_id and not attachment.is_removed]

class InMemoryChangeRecordRepository(InMemoryRepository[ChangeRecord], ChangeRecordRepository):
    """In-memory implementation of ChangeRecordRepository."""
    
    def get_by_opportunity(self, opportunity_id: uuid.UUID) -> List[ChangeRecord]:
        """Get change records by opportunity."""
        return [record for record in self._entities.values() 
                if record.opportunity_id == opportunity_id]
    
    def get_by_field(self, opportunity_id: uuid.UUID, field: str) -> List[ChangeRecord]:
        """Get change records by field for an opportunity."""
        return [record for record in self._entities.values() 
                if record.opportunity_id == opportunity_id and record.field_changed == field]
    
    def get_by_user(self, user_id: uuid.UUID) -> List[ChangeRecord]:
        """Get change records by user."""
        return [record for record in self._entities.values() 
                if record.changed_by == user_id]
