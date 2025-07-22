"""
Opportunity validation service for complex business validation logic.
"""

from typing import List, Dict, Any, Optional
from decimal import Decimal
import logging

from ..entities.opportunity import Opportunity
from ..enums.status import OpportunityStatus
from ..enums.priority import Priority


class OpportunityValidationService:
    """Service for validating opportunity business rules and constraints."""
    
    def __init__(self):
        """Initialize the validation service."""
        self.logger = logging.getLogger(__name__)
    
    def validate_for_creation(self, opportunity_data: Dict[str, Any]) -> List[str]:
        """Validate opportunity data for creation."""
        errors = []
        
        # Basic field validation
        if not opportunity_data.get('title', '').strip():
            errors.append("Opportunity title is required")
        
        if not opportunity_data.get('description', '').strip():
            errors.append("Opportunity description is required")
        
        if not opportunity_data.get('customer_id', '').strip():
            errors.append("Customer ID is required")
        
        if not opportunity_data.get('sales_manager_id', '').strip():
            errors.append("Sales Manager ID is required")
        
        # ARR validation
        try:
            arr = Decimal(str(opportunity_data.get('annual_recurring_revenue', 0)))
            if arr <= 0:
                errors.append("Annual Recurring Revenue must be positive")
        except (ValueError, TypeError):
            errors.append("Annual Recurring Revenue must be a valid number")
        
        # Priority validation
        priority_str = opportunity_data.get('priority')
        if priority_str:
            try:
                Priority.from_string(priority_str)
            except ValueError:
                errors.append(f"Invalid priority: {priority_str}")
        else:
            errors.append("Priority is required")
        
        return errors
    
    def validate_for_submission(self, opportunity: Opportunity) -> List[str]:
        """Validate opportunity for submission to matching process."""
        errors = []
        
        # Status validation
        if opportunity.status != OpportunityStatus.DRAFT:
            errors.append("Only draft opportunities can be submitted")
        
        # Problem statement validation
        if not opportunity.problem_statement:
            errors.append("Problem statement is required for submission")
        elif not opportunity.problem_statement.is_complete:
            errors.append("Problem statement must be complete with all sections filled")
        
        # Skills validation
        if not opportunity.skill_requirements:
            errors.append("At least one skill requirement must be specified")
        
        mandatory_skills = opportunity.mandatory_skills
        if not mandatory_skills:
            errors.append("At least one mandatory skill requirement must be specified")
        
        # Timeline validation
        if not opportunity.timeline_specification:
            errors.append("Timeline specification is required for submission")
        
        return errors
    
    def validate_for_modification(self, opportunity: Opportunity, 
                                 modification_data: Dict[str, Any]) -> List[str]:
        """Validate opportunity modification based on current status."""
        errors = []
        
        # Status-based modification rules
        if not opportunity.status.is_modifiable:
            # Limited modifications allowed after architect selection
            if opportunity.status == OpportunityStatus.ARCHITECT_SELECTED:
                allowed_fields = ['priority', 'notes']
                for field in modification_data.keys():
                    if field not in allowed_fields:
                        errors.append(f"Field '{field}' cannot be modified after architect selection")
            else:
                errors.append(f"Opportunity cannot be modified in {opportunity.status} status")
        
        # Validate specific field changes
        if 'annual_recurring_revenue' in modification_data:
            try:
                arr = Decimal(str(modification_data['annual_recurring_revenue']))
                if arr <= 0:
                    errors.append("Annual Recurring Revenue must be positive")
            except (ValueError, TypeError):
                errors.append("Annual Recurring Revenue must be a valid number")
        
        return errors
    
    def validate_status_transition(self, opportunity: Opportunity, 
                                  new_status: OpportunityStatus) -> List[str]:
        """Validate status transition rules."""
        errors = []
        
        if not opportunity.status.can_transition_to(new_status):
            errors.append(f"Invalid status transition from {opportunity.status} to {new_status}")
        
        # Additional business rules for specific transitions
        if new_status == OpportunityStatus.MATCHING_IN_PROGRESS:
            if not opportunity.is_ready_for_matching:
                errors.append("Opportunity is not ready for matching process")
        
        if new_status == OpportunityStatus.ARCHITECT_SELECTED:
            if not opportunity.selected_architect_id:
                errors.append("Architect must be selected before changing to ARCHITECT_SELECTED status")
        
        return errors
    
    def validate_cancellation(self, opportunity: Opportunity, reason: str) -> List[str]:
        """Validate opportunity cancellation."""
        errors = []
        
        if opportunity.status.is_final:
            errors.append("Cannot cancel a completed or already cancelled opportunity")
        
        if not reason or not reason.strip():
            errors.append("Cancellation reason is required")
        
        return errors
    
    def validate_reactivation(self, opportunity: Opportunity) -> List[str]:
        """Validate opportunity reactivation."""
        errors = []
        
        if opportunity.status != OpportunityStatus.CANCELLED:
            errors.append("Only cancelled opportunities can be reactivated")
        
        if not opportunity.cancellation_date:
            errors.append("Cancellation date not found")
        else:
            from datetime import date
            days_since_cancellation = (date.today() - opportunity.cancellation_date).days
            if days_since_cancellation > 90:
                errors.append("Cannot reactivate opportunity after 90 days")
        
        return errors
    
    def validate_architect_selection(self, opportunity: Opportunity, 
                                   architect_id: str) -> List[str]:
        """Validate architect selection."""
        errors = []
        
        if opportunity.status != OpportunityStatus.MATCHES_FOUND:
            errors.append("Can only select architect when matches are found")
        
        if not architect_id or not architect_id.strip():
            errors.append("Architect ID is required")
        
        return errors
    
    def validate_completion(self, opportunity: Opportunity) -> List[str]:
        """Validate opportunity completion."""
        errors = []
        
        if opportunity.status != OpportunityStatus.ARCHITECT_SELECTED:
            errors.append("Can only complete opportunity after architect is selected")
        
        return errors
    
    def validate_business_rules(self, opportunity: Opportunity) -> List[str]:
        """Validate general business rules."""
        errors = []
        
        # High priority opportunities should have complete problem statements
        if (opportunity.priority == Priority.CRITICAL and 
            opportunity.problem_statement and 
            not opportunity.problem_statement.is_complete):
            errors.append("Critical priority opportunities must have complete problem statements")
        
        # Timeline validation for high-value opportunities
        if (opportunity.annual_recurring_revenue > Decimal('1000000') and 
            opportunity.timeline_specification and 
            opportunity.timeline_specification.total_duration_days < 30):
            errors.append("High-value opportunities (>$1M ARR) should have timeline of at least 30 days")
        
        return errors
    
    def get_validation_summary(self, opportunity: Opportunity) -> Dict[str, Any]:
        """Get a comprehensive validation summary for an opportunity."""
        return {
            "is_valid_for_submission": len(self.validate_for_submission(opportunity)) == 0,
            "is_ready_for_matching": opportunity.is_ready_for_matching,
            "business_rule_violations": self.validate_business_rules(opportunity),
            "status": opportunity.status.value,
            "is_modifiable": opportunity.status.is_modifiable
        }
