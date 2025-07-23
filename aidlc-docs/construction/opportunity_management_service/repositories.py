"""
Repository interfaces for the Opportunity Management Service.
"""

import uuid
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, TypeVar, Generic

from .common import Repository
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

# Type variables for generic repositories
T_User = TypeVar('T_User', bound=User)
T_Customer = TypeVar('T_Customer', bound=Customer)
T_SkillsCatalog = TypeVar('T_SkillsCatalog', bound=SkillsCatalog)
T_Opportunity = TypeVar('T_Opportunity', bound=Opportunity)
T_ProblemStatement = TypeVar('T_ProblemStatement', bound=ProblemStatement)
T_SkillRequirement = TypeVar('T_SkillRequirement', bound=SkillRequirement)
T_TimelineRequirement = TypeVar('T_TimelineRequirement', bound=TimelineRequirement)
T_OpportunityStatus = TypeVar('T_OpportunityStatus', bound=OpportunityStatus)
T_Attachment = TypeVar('T_Attachment', bound=Attachment)
T_ChangeRecord = TypeVar('T_ChangeRecord', bound=ChangeRecord)

class UserRepository(Repository[T_User], ABC):
    """Repository interface for User entities."""
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[T_User]:
        """Get a user by email."""
        pass
    
    @abstractmethod
    def get_by_employee_id(self, employee_id: str) -> Optional[T_User]:
        """Get a user by employee ID."""
        pass
    
    @abstractmethod
    def get_sales_managers(self) -> List[T_User]:
        """Get all sales managers."""
        pass
    
    @abstractmethod
    def get_solution_architects(self) -> List[T_User]:
        """Get all solution architects."""
        pass

class CustomerRepository(Repository[T_Customer], ABC):
    """Repository interface for Customer entities."""
    
    @abstractmethod
    def get_by_name(self, name: str) -> List[T_Customer]:
        """Get customers by name (partial match)."""
        pass
    
    @abstractmethod
    def get_active_customers(self) -> List[T_Customer]:
        """Get all active customers."""
        pass

class SkillsCatalogRepository(Repository[T_SkillsCatalog], ABC):
    """Repository interface for SkillsCatalog entities."""
    
    @abstractmethod
    def get_by_name(self, name: str) -> List[T_SkillsCatalog]:
        """Get skills by name (partial match)."""
        pass
    
    @abstractmethod
    def get_by_category(self, category: str) -> List[T_SkillsCatalog]:
        """Get skills by category."""
        pass
    
    @abstractmethod
    def get_active_skills(self) -> List[T_SkillsCatalog]:
        """Get all active skills."""
        pass
    
    @abstractmethod
    def search_skills(self, query: str) -> List[T_SkillsCatalog]:
        """Search skills by name, category, or description."""
        pass

class OpportunityRepository(Repository[T_Opportunity], ABC):
    """Repository interface for Opportunity entities."""
    
    @abstractmethod
    def get_by_sales_manager(self, sales_manager_id: uuid.UUID) -> List[T_Opportunity]:
        """Get opportunities by sales manager."""
        pass
    
    @abstractmethod
    def get_by_customer(self, customer_id: uuid.UUID) -> List[T_Opportunity]:
        """Get opportunities by customer."""
        pass
    
    @abstractmethod
    def get_by_status(self, status: str) -> List[T_Opportunity]:
        """Get opportunities by status."""
        pass
    
    @abstractmethod
    def get_by_priority(self, priority: str) -> List[T_Opportunity]:
        """Get opportunities by priority."""
        pass
    
    @abstractmethod
    def search_opportunities(self, query: str) -> List[T_Opportunity]:
        """Search opportunities by title or description."""
        pass

class ProblemStatementRepository(Repository[T_ProblemStatement], ABC):
    """Repository interface for ProblemStatement entities."""
    
    @abstractmethod
    def get_by_opportunity(self, opportunity_id: uuid.UUID) -> Optional[T_ProblemStatement]:
        """Get problem statement by opportunity."""
        pass
    
    @abstractmethod
    def search_problem_statements(self, query: str) -> List[T_ProblemStatement]:
        """Search problem statements by content."""
        pass

class SkillRequirementRepository(Repository[T_SkillRequirement], ABC):
    """Repository interface for SkillRequirement entities."""
    
    @abstractmethod
    def get_by_opportunity(self, opportunity_id: uuid.UUID) -> List[T_SkillRequirement]:
        """Get skill requirements by opportunity."""
        pass
    
    @abstractmethod
    def get_by_skill(self, skill_id: uuid.UUID) -> List[T_SkillRequirement]:
        """Get skill requirements by skill."""
        pass
    
    @abstractmethod
    def get_must_have_skills(self, opportunity_id: uuid.UUID) -> List[T_SkillRequirement]:
        """Get 'Must Have' skill requirements for an opportunity."""
        pass

class TimelineRequirementRepository(Repository[T_TimelineRequirement], ABC):
    """Repository interface for TimelineRequirement entities."""
    
    @abstractmethod
    def get_by_opportunity(self, opportunity_id: uuid.UUID) -> Optional[T_TimelineRequirement]:
        """Get timeline requirement by opportunity."""
        pass
    
    @abstractmethod
    def get_by_date_range(self, start_date: str, end_date: str) -> List[T_TimelineRequirement]:
        """Get timeline requirements within a date range."""
        pass

class OpportunityStatusRepository(Repository[T_OpportunityStatus], ABC):
    """Repository interface for OpportunityStatus entities."""
    
    @abstractmethod
    def get_by_opportunity(self, opportunity_id: uuid.UUID) -> List[T_OpportunityStatus]:
        """Get status records by opportunity."""
        pass
    
    @abstractmethod
    def get_current_status(self, opportunity_id: uuid.UUID) -> Optional[T_OpportunityStatus]:
        """Get the current status record for an opportunity."""
        pass
    
    @abstractmethod
    def get_status_history(self, opportunity_id: uuid.UUID) -> List[T_OpportunityStatus]:
        """Get the complete status history for an opportunity."""
        pass

class AttachmentRepository(Repository[T_Attachment], ABC):
    """Repository interface for Attachment entities."""
    
    @abstractmethod
    def get_by_problem_statement(self, problem_statement_id: uuid.UUID) -> List[T_Attachment]:
        """Get attachments by problem statement."""
        pass
    
    @abstractmethod
    def get_by_file_type(self, file_type: str) -> List[T_Attachment]:
        """Get attachments by file type."""
        pass
    
    @abstractmethod
    def get_active_attachments(self, problem_statement_id: uuid.UUID) -> List[T_Attachment]:
        """Get active (not removed) attachments for a problem statement."""
        pass

class ChangeRecordRepository(Repository[T_ChangeRecord], ABC):
    """Repository interface for ChangeRecord entities."""
    
    @abstractmethod
    def get_by_opportunity(self, opportunity_id: uuid.UUID) -> List[T_ChangeRecord]:
        """Get change records by opportunity."""
        pass
    
    @abstractmethod
    def get_by_field(self, opportunity_id: uuid.UUID, field: str) -> List[T_ChangeRecord]:
        """Get change records by field for an opportunity."""
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: uuid.UUID) -> List[T_ChangeRecord]:
        """Get change records by user."""
        pass
