"""
Opportunity repository interface for data access abstraction.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import date

from ...domain.entities.opportunity import Opportunity
from ...domain.enums.status import OpportunityStatus
from ...domain.enums.priority import Priority


class OpportunityRepository(ABC):
    """Abstract base class for opportunity repository implementations."""
    
    @abstractmethod
    def save(self, opportunity: Opportunity) -> Opportunity:
        """Save an opportunity to the repository."""
        pass
    
    @abstractmethod
    def find_by_id(self, opportunity_id: str) -> Optional[Opportunity]:
        """Find an opportunity by its ID."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Opportunity]:
        """Find all opportunities."""
        pass
    
    @abstractmethod
    def find_by_sales_manager(self, sales_manager_id: str) -> List[Opportunity]:
        """Find all opportunities for a specific sales manager."""
        pass
    
    @abstractmethod
    def find_by_customer(self, customer_id: str) -> List[Opportunity]:
        """Find all opportunities for a specific customer."""
        pass
    
    @abstractmethod
    def find_by_status(self, status: OpportunityStatus) -> List[Opportunity]:
        """Find all opportunities with a specific status."""
        pass
    
    @abstractmethod
    def find_by_priority(self, priority: Priority) -> List[Opportunity]:
        """Find all opportunities with a specific priority."""
        pass
    
    @abstractmethod
    def find_by_architect(self, architect_id: str) -> List[Opportunity]:
        """Find all opportunities assigned to a specific architect."""
        pass
    
    @abstractmethod
    def find_ready_for_matching(self) -> List[Opportunity]:
        """Find all opportunities ready for matching process."""
        pass
    
    @abstractmethod
    def find_by_date_range(self, start_date: date, end_date: date) -> List[Opportunity]:
        """Find opportunities created within a date range."""
        pass
    
    @abstractmethod
    def find_cancelled_within_reactivation_period(self) -> List[Opportunity]:
        """Find cancelled opportunities that can still be reactivated."""
        pass
    
    @abstractmethod
    def search(self, criteria: Dict[str, Any]) -> List[Opportunity]:
        """Search opportunities based on multiple criteria."""
        pass
    
    @abstractmethod
    def delete(self, opportunity_id: str) -> bool:
        """Delete an opportunity from the repository."""
        pass
    
    @abstractmethod
    def exists(self, opportunity_id: str) -> bool:
        """Check if an opportunity exists in the repository."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Get the total count of opportunities."""
        pass
    
    @abstractmethod
    def count_by_status(self, status: OpportunityStatus) -> int:
        """Get count of opportunities by status."""
        pass
    
    @abstractmethod
    def count_by_sales_manager(self, sales_manager_id: str) -> int:
        """Get count of opportunities by sales manager."""
        pass
    
    # Advanced query methods
    
    @abstractmethod
    def find_high_value_opportunities(self, min_arr: float = 500000) -> List[Opportunity]:
        """Find high-value opportunities above specified ARR threshold."""
        pass
    
    @abstractmethod
    def find_overdue_opportunities(self) -> List[Opportunity]:
        """Find opportunities that are overdue based on their timeline."""
        pass
    
    @abstractmethod
    def find_by_skill_requirement(self, skill_name: str) -> List[Opportunity]:
        """Find opportunities requiring a specific skill."""
        pass
    
    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """Get repository statistics."""
        pass
