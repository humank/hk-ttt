"""
Opportunity query service for read operations and dashboard functionality.
"""

from typing import Dict, Any, List, Optional
from datetime import date, datetime, timedelta
import logging

from ...infrastructure.repositories.opportunity_repository import OpportunityRepository
from ...infrastructure.repositories.customer_repository import CustomerRepository
from ...domain.enums.status import OpportunityStatus
from ...domain.enums.priority import Priority


class OpportunityQueryService:
    """Service for querying opportunities and providing dashboard functionality."""
    
    def __init__(self, 
                 opportunity_repository: OpportunityRepository,
                 customer_repository: CustomerRepository):
        """Initialize the query service with repositories."""
        self.opportunity_repository = opportunity_repository
        self.customer_repository = customer_repository
        self.logger = logging.getLogger(__name__)
    
    def get_opportunity_by_id(self, opportunity_id: str) -> Optional[Dict[str, Any]]:
        """Get opportunity details by ID."""
        opportunity = self.opportunity_repository.find_by_id(opportunity_id)
        if not opportunity:
            return None
        
        # Enrich with customer information
        customer = self.customer_repository.find_by_id(opportunity.customer_id)
        opportunity_dict = opportunity.to_dict()
        opportunity_dict["customer"] = customer.to_dict() if customer else None
        
        return opportunity_dict
    
    def get_sales_manager_dashboard(self, sales_manager_id: str) -> Dict[str, Any]:
        """Get dashboard data for a sales manager (US-SM-7: Opportunity Status Tracking)."""
        self.logger.info(f"Getting dashboard for sales manager {sales_manager_id}")
        
        # Get all opportunities for the sales manager
        opportunities = self.opportunity_repository.find_by_sales_manager(sales_manager_id)
        
        # Count by status
        status_counts = {}
        for status in OpportunityStatus:
            count = len([opp for opp in opportunities if opp.status == status])
            status_counts[status.value] = count
        
        # Count by priority
        priority_counts = {}
        for priority in Priority:
            count = len([opp for opp in opportunities if opp.priority == priority])
            priority_counts[priority.value] = count
        
        # Recent opportunities (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_opportunities = [
            opp for opp in opportunities 
            if opp.created_at >= thirty_days_ago
        ]
        
        # Opportunities requiring attention
        requiring_attention = []
        for opp in opportunities:
            if opp.status == OpportunityStatus.DRAFT and opp.age_in_days > 7:
                requiring_attention.append({
                    "id": opp.id,
                    "title": opp.title,
                    "reason": "Draft for more than 7 days",
                    "age_days": opp.age_in_days
                })
            elif (opp.status == OpportunityStatus.MATCHES_FOUND and 
                  opp.age_in_days > 3):
                requiring_attention.append({
                    "id": opp.id,
                    "title": opp.title,
                    "reason": "Matches found but no architect selected",
                    "age_days": opp.age_in_days
                })
        
        # Calculate total ARR
        total_arr = sum(opp.annual_recurring_revenue for opp in opportunities)
        active_arr = sum(
            opp.annual_recurring_revenue for opp in opportunities 
            if opp.status not in [OpportunityStatus.CANCELLED, OpportunityStatus.COMPLETED]
        )
        
        return {
            "sales_manager_id": sales_manager_id,
            "summary": {
                "total_opportunities": len(opportunities),
                "active_opportunities": len([opp for opp in opportunities if not opp.status.is_final]),
                "completed_opportunities": status_counts.get("Completed", 0),
                "cancelled_opportunities": status_counts.get("Cancelled", 0),
                "total_arr": float(total_arr),
                "active_arr": float(active_arr)
            },
            "by_status": status_counts,
            "by_priority": priority_counts,
            "recent_opportunities": [opp.to_dict() for opp in recent_opportunities[-5:]],
            "requiring_attention": requiring_attention,
            "high_value_opportunities": len([
                opp for opp in opportunities 
                if opp.annual_recurring_revenue >= 500000
            ])
        }
    
    def search_opportunities(self, criteria: Dict[str, Any], 
                           user_id: Optional[str] = None) -> Dict[str, Any]:
        """Search opportunities with filtering and pagination."""
        self.logger.info("Searching opportunities with criteria")
        
        # Add user filter if provided
        if user_id and 'sales_manager_id' not in criteria:
            criteria['sales_manager_id'] = user_id
        
        # Perform search
        opportunities = self.opportunity_repository.search(criteria)
        
        # Apply sorting
        sort_by = criteria.get('sort_by', 'created_at')
        sort_order = criteria.get('sort_order', 'desc')
        
        if sort_by == 'created_at':
            opportunities.sort(key=lambda x: x.created_at, reverse=(sort_order == 'desc'))
        elif sort_by == 'priority':
            opportunities.sort(key=lambda x: x.priority.weight, reverse=(sort_order == 'desc'))
        elif sort_by == 'arr':
            opportunities.sort(key=lambda x: x.annual_recurring_revenue, reverse=(sort_order == 'desc'))
        elif sort_by == 'title':
            opportunities.sort(key=lambda x: x.title.lower(), reverse=(sort_order == 'desc'))
        
        # Apply pagination
        page = criteria.get('page', 1)
        page_size = criteria.get('page_size', 20)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        paginated_opportunities = opportunities[start_index:end_index]
        
        # Enrich with customer data
        enriched_opportunities = []
        for opp in paginated_opportunities:
            opp_dict = opp.to_dict()
            customer = self.customer_repository.find_by_id(opp.customer_id)
            opp_dict["customer_name"] = customer.name if customer else "Unknown"
            enriched_opportunities.append(opp_dict)
        
        return {
            "opportunities": enriched_opportunities,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": len(opportunities),
                "total_pages": (len(opportunities) + page_size - 1) // page_size,
                "has_next": end_index < len(opportunities),
                "has_previous": page > 1
            },
            "filters_applied": criteria
        }
    
    def get_opportunity_statistics(self) -> Dict[str, Any]:
        """Get overall opportunity statistics."""
        self.logger.info("Getting opportunity statistics")
        
        stats = self.opportunity_repository.get_statistics()
        
        # Add time-based statistics
        today = date.today()
        this_month_start = today.replace(day=1)
        last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
        
        this_month_opportunities = self.opportunity_repository.find_by_date_range(
            this_month_start, today
        )
        last_month_opportunities = self.opportunity_repository.find_by_date_range(
            last_month_start, this_month_start - timedelta(days=1)
        )
        
        stats.update({
            "this_month_count": len(this_month_opportunities),
            "last_month_count": len(last_month_opportunities),
            "month_over_month_change": len(this_month_opportunities) - len(last_month_opportunities),
            "ready_for_matching": len(self.opportunity_repository.find_ready_for_matching()),
            "reactivatable_cancelled": len(self.opportunity_repository.find_cancelled_within_reactivation_period())
        })
        
        return stats
    
    def get_opportunities_by_status(self, status: str, 
                                  sales_manager_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get opportunities filtered by status."""
        try:
            opportunity_status = OpportunityStatus.from_string(status)
            opportunities = self.opportunity_repository.find_by_status(opportunity_status)
            
            # Filter by sales manager if provided
            if sales_manager_id:
                opportunities = [
                    opp for opp in opportunities 
                    if opp.sales_manager_id == sales_manager_id
                ]
            
            # Enrich with customer data
            enriched_opportunities = []
            for opp in opportunities:
                opp_dict = opp.to_dict()
                customer = self.customer_repository.find_by_id(opp.customer_id)
                opp_dict["customer_name"] = customer.name if customer else "Unknown"
                enriched_opportunities.append(opp_dict)
            
            return enriched_opportunities
            
        except ValueError:
            self.logger.error(f"Invalid status: {status}")
            return []
    
    def get_high_priority_opportunities(self, 
                                      sales_manager_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get high priority opportunities."""
        high_priority_opportunities = []
        
        for priority in [Priority.HIGH, Priority.CRITICAL]:
            opportunities = self.opportunity_repository.find_by_priority(priority)
            
            # Filter by sales manager if provided
            if sales_manager_id:
                opportunities = [
                    opp for opp in opportunities 
                    if opp.sales_manager_id == sales_manager_id
                ]
            
            high_priority_opportunities.extend(opportunities)
        
        # Sort by priority weight (highest first)
        high_priority_opportunities.sort(key=lambda x: x.priority.weight, reverse=True)
        
        # Enrich with customer data
        enriched_opportunities = []
        for opp in high_priority_opportunities:
            opp_dict = opp.to_dict()
            customer = self.customer_repository.find_by_id(opp.customer_id)
            opp_dict["customer_name"] = customer.name if customer else "Unknown"
            enriched_opportunities.append(opp_dict)
        
        return enriched_opportunities
    
    def get_overdue_opportunities(self, 
                                sales_manager_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get overdue opportunities."""
        overdue_opportunities = self.opportunity_repository.find_overdue_opportunities()
        
        # Filter by sales manager if provided
        if sales_manager_id:
            overdue_opportunities = [
                opp for opp in overdue_opportunities 
                if opp.sales_manager_id == sales_manager_id
            ]
        
        # Enrich with customer data and calculate days overdue
        enriched_opportunities = []
        today = date.today()
        
        for opp in overdue_opportunities:
            opp_dict = opp.to_dict()
            customer = self.customer_repository.find_by_id(opp.customer_id)
            opp_dict["customer_name"] = customer.name if customer else "Unknown"
            
            if opp.timeline_specification:
                days_overdue = (today - opp.timeline_specification.expected_start_date).days
                opp_dict["days_overdue"] = days_overdue
            
            enriched_opportunities.append(opp_dict)
        
        # Sort by days overdue (most overdue first)
        enriched_opportunities.sort(key=lambda x: x.get("days_overdue", 0), reverse=True)
        
        return enriched_opportunities
    
    def get_opportunities_requiring_attention(self, 
                                            sales_manager_id: str) -> List[Dict[str, Any]]:
        """Get opportunities that require immediate attention."""
        opportunities = self.opportunity_repository.find_by_sales_manager(sales_manager_id)
        requiring_attention = []
        
        for opp in opportunities:
            attention_reasons = []
            
            # Draft for too long
            if opp.status == OpportunityStatus.DRAFT and opp.age_in_days > 7:
                attention_reasons.append(f"Draft for {opp.age_in_days} days")
            
            # Matches found but no selection
            if opp.status == OpportunityStatus.MATCHES_FOUND and opp.age_in_days > 3:
                attention_reasons.append("Matches found - architect selection pending")
            
            # High priority not progressing
            if (opp.priority in [Priority.HIGH, Priority.CRITICAL] and
                opp.status == OpportunityStatus.SUBMITTED and opp.age_in_days > 2):
                attention_reasons.append("High priority opportunity not progressing")
            
            # Overdue timeline
            if (opp.timeline_specification and 
                opp.timeline_specification.expected_start_date < date.today() and
                opp.status not in [OpportunityStatus.COMPLETED, OpportunityStatus.CANCELLED]):
                attention_reasons.append("Timeline overdue")
            
            if attention_reasons:
                opp_dict = opp.to_dict()
                customer = self.customer_repository.find_by_id(opp.customer_id)
                opp_dict["customer_name"] = customer.name if customer else "Unknown"
                opp_dict["attention_reasons"] = attention_reasons
                requiring_attention.append(opp_dict)
        
        # Sort by priority and age
        requiring_attention.sort(
            key=lambda x: (x["priority"] == "Critical", x["priority"] == "High", x["age_in_days"]),
            reverse=True
        )
        
        return requiring_attention
