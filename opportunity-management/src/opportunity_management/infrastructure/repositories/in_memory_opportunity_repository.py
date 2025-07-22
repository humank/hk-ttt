"""
In-memory implementation of the opportunity repository.
"""

from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from decimal import Decimal
import logging

from .opportunity_repository import OpportunityRepository
from ...domain.entities.opportunity import Opportunity
from ...domain.enums.status import OpportunityStatus
from ...domain.enums.priority import Priority


class InMemoryOpportunityRepository(OpportunityRepository):
    """In-memory implementation of opportunity repository using dictionaries."""
    
    def __init__(self):
        """Initialize the in-memory repository."""
        self._opportunities: Dict[str, Opportunity] = {}
        self.logger = logging.getLogger(__name__)
    
    def save(self, opportunity: Opportunity) -> Opportunity:
        """Save an opportunity to the repository."""
        self.logger.debug(f"Saving opportunity {opportunity.id}")
        
        # Update timestamp if this is an existing opportunity
        if opportunity.id in self._opportunities:
            opportunity.update_timestamp()
        
        self._opportunities[opportunity.id] = opportunity
        return opportunity
    
    def find_by_id(self, opportunity_id: str) -> Optional[Opportunity]:
        """Find an opportunity by its ID."""
        return self._opportunities.get(opportunity_id)
    
    def find_all(self) -> List[Opportunity]:
        """Find all opportunities."""
        return list(self._opportunities.values())
    
    def find_by_sales_manager(self, sales_manager_id: str) -> List[Opportunity]:
        """Find all opportunities for a specific sales manager."""
        return [
            opp for opp in self._opportunities.values()
            if opp.sales_manager_id == sales_manager_id
        ]
    
    def find_by_customer(self, customer_id: str) -> List[Opportunity]:
        """Find all opportunities for a specific customer."""
        return [
            opp for opp in self._opportunities.values()
            if opp.customer_id == customer_id
        ]
    
    def find_by_status(self, status: OpportunityStatus) -> List[Opportunity]:
        """Find all opportunities with a specific status."""
        return [
            opp for opp in self._opportunities.values()
            if opp.status == status
        ]
    
    def find_by_priority(self, priority: Priority) -> List[Opportunity]:
        """Find all opportunities with a specific priority."""
        return [
            opp for opp in self._opportunities.values()
            if opp.priority == priority
        ]
    
    def find_by_architect(self, architect_id: str) -> List[Opportunity]:
        """Find all opportunities assigned to a specific architect."""
        return [
            opp for opp in self._opportunities.values()
            if opp.selected_architect_id == architect_id
        ]
    
    def find_ready_for_matching(self) -> List[Opportunity]:
        """Find all opportunities ready for matching process."""
        return [
            opp for opp in self._opportunities.values()
            if opp.is_ready_for_matching
        ]
    
    def find_by_date_range(self, start_date: date, end_date: date) -> List[Opportunity]:
        """Find opportunities created within a date range."""
        return [
            opp for opp in self._opportunities.values()
            if start_date <= opp.created_at.date() <= end_date
        ]
    
    def find_cancelled_within_reactivation_period(self) -> List[Opportunity]:
        """Find cancelled opportunities that can still be reactivated."""
        cutoff_date = date.today() - timedelta(days=90)
        
        return [
            opp for opp in self._opportunities.values()
            if (opp.status == OpportunityStatus.CANCELLED and
                opp.cancellation_date and
                opp.cancellation_date >= cutoff_date)
        ]
    
    def search(self, criteria: Dict[str, Any]) -> List[Opportunity]:
        """Search opportunities based on multiple criteria."""
        results = list(self._opportunities.values())
        
        # Filter by status
        if 'status' in criteria:
            status = OpportunityStatus.from_string(criteria['status'])
            results = [opp for opp in results if opp.status == status]
        
        # Filter by priority
        if 'priority' in criteria:
            priority = Priority.from_string(criteria['priority'])
            results = [opp for opp in results if opp.priority == priority]
        
        # Filter by sales manager
        if 'sales_manager_id' in criteria:
            results = [opp for opp in results if opp.sales_manager_id == criteria['sales_manager_id']]
        
        # Filter by customer
        if 'customer_id' in criteria:
            results = [opp for opp in results if opp.customer_id == criteria['customer_id']]
        
        # Filter by title (partial match)
        if 'title_contains' in criteria:
            title_pattern = criteria['title_contains'].lower()
            results = [opp for opp in results if title_pattern in opp.title.lower()]
        
        # Filter by ARR range
        if 'min_arr' in criteria:
            min_arr = Decimal(str(criteria['min_arr']))
            results = [opp for opp in results if opp.annual_recurring_revenue >= min_arr]
        
        if 'max_arr' in criteria:
            max_arr = Decimal(str(criteria['max_arr']))
            results = [opp for opp in results if opp.annual_recurring_revenue <= max_arr]
        
        # Filter by creation date range
        if 'created_after' in criteria:
            created_after = datetime.fromisoformat(criteria['created_after'])
            results = [opp for opp in results if opp.created_at >= created_after]
        
        if 'created_before' in criteria:
            created_before = datetime.fromisoformat(criteria['created_before'])
            results = [opp for opp in results if opp.created_at <= created_before]
        
        # Filter by architect
        if 'architect_id' in criteria:
            results = [opp for opp in results if opp.selected_architect_id == criteria['architect_id']]
        
        return results
    
    def delete(self, opportunity_id: str) -> bool:
        """Delete an opportunity from the repository."""
        if opportunity_id in self._opportunities:
            del self._opportunities[opportunity_id]
            self.logger.debug(f"Deleted opportunity {opportunity_id}")
            return True
        return False
    
    def exists(self, opportunity_id: str) -> bool:
        """Check if an opportunity exists in the repository."""
        return opportunity_id in self._opportunities
    
    def count(self) -> int:
        """Get the total count of opportunities."""
        return len(self._opportunities)
    
    def count_by_status(self, status: OpportunityStatus) -> int:
        """Get count of opportunities by status."""
        return len(self.find_by_status(status))
    
    def count_by_sales_manager(self, sales_manager_id: str) -> int:
        """Get count of opportunities by sales manager."""
        return len(self.find_by_sales_manager(sales_manager_id))
    
    # Advanced query methods
    
    def find_high_value_opportunities(self, min_arr: float = 500000) -> List[Opportunity]:
        """Find high-value opportunities above specified ARR threshold."""
        min_arr_decimal = Decimal(str(min_arr))
        return [
            opp for opp in self._opportunities.values()
            if opp.annual_recurring_revenue >= min_arr_decimal
        ]
    
    def find_overdue_opportunities(self) -> List[Opportunity]:
        """Find opportunities that are overdue based on their timeline."""
        today = date.today()
        overdue_opportunities = []
        
        for opp in self._opportunities.values():
            if (opp.timeline_specification and
                opp.status not in [OpportunityStatus.COMPLETED, OpportunityStatus.CANCELLED] and
                opp.timeline_specification.expected_start_date < today):
                overdue_opportunities.append(opp)
        
        return overdue_opportunities
    
    def find_by_skill_requirement(self, skill_name: str) -> List[Opportunity]:
        """Find opportunities requiring a specific skill."""
        skill_name_lower = skill_name.lower()
        return [
            opp for opp in self._opportunities.values()
            if any(skill.skill_name.lower() == skill_name_lower 
                  for skill in opp.skill_requirements)
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get repository statistics."""
        total_count = len(self._opportunities)
        
        if total_count == 0:
            return {
                "total_opportunities": 0,
                "by_status": {},
                "by_priority": {},
                "high_value_count": 0,
                "overdue_count": 0
            }
        
        # Count by status
        status_counts = {}
        for status in OpportunityStatus:
            status_counts[status.value] = self.count_by_status(status)
        
        # Count by priority
        priority_counts = {}
        for priority in Priority:
            count = len([opp for opp in self._opportunities.values() if opp.priority == priority])
            priority_counts[priority.value] = count
        
        # High value opportunities
        high_value_count = len(self.find_high_value_opportunities())
        
        # Overdue opportunities
        overdue_count = len(self.find_overdue_opportunities())
        
        # Average ARR
        total_arr = sum(opp.annual_recurring_revenue for opp in self._opportunities.values())
        avg_arr = total_arr / total_count if total_count > 0 else 0
        
        return {
            "total_opportunities": total_count,
            "by_status": status_counts,
            "by_priority": priority_counts,
            "high_value_count": high_value_count,
            "overdue_count": overdue_count,
            "average_arr": float(avg_arr),
            "total_arr": float(total_arr)
        }
    
    def clear(self) -> None:
        """Clear all opportunities from the repository (for testing)."""
        self._opportunities.clear()
        self.logger.debug("Cleared all opportunities from repository")
    
    def bulk_save(self, opportunities: List[Opportunity]) -> List[Opportunity]:
        """Save multiple opportunities at once."""
        saved_opportunities = []
        for opportunity in opportunities:
            saved_opportunities.append(self.save(opportunity))
        return saved_opportunities
