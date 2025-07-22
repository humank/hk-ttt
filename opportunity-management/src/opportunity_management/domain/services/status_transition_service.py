"""
Status transition service for orchestrating opportunity status changes.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date
import logging

from ..entities.opportunity import Opportunity
from ..enums.status import OpportunityStatus
from ..entities.status_history import StatusHistory
from .opportunity_validation_service import OpportunityValidationService


class StatusTransitionService:
    """Service for orchestrating opportunity status transitions with business rules."""
    
    def __init__(self, validation_service: OpportunityValidationService):
        """Initialize the status transition service."""
        self.validation_service = validation_service
        self.logger = logging.getLogger(__name__)
    
    def submit_opportunity(self, opportunity: Opportunity, submitted_by: str) -> Dict[str, Any]:
        """Submit opportunity for matching process."""
        self.logger.info(f"Attempting to submit opportunity {opportunity.id}")
        
        # Validate opportunity for submission
        validation_errors = self.validation_service.validate_for_submission(opportunity)
        if validation_errors:
            return {
                "success": False,
                "errors": validation_errors,
                "status": opportunity.status.value
            }
        
        try:
            # Change status to submitted
            opportunity.change_status(
                new_status=OpportunityStatus.SUBMITTED,
                changed_by=submitted_by,
                reason="Opportunity submitted for matching",
                notes="All required information provided"
            )
            
            self.logger.info(f"Opportunity {opportunity.id} successfully submitted")
            
            return {
                "success": True,
                "message": "Opportunity submitted successfully",
                "status": opportunity.status.value,
                "next_steps": ["Matching process will begin", "You will be notified when matches are found"]
            }
            
        except Exception as e:
            self.logger.error(f"Error submitting opportunity {opportunity.id}: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "status": opportunity.status.value
            }
    
    def start_matching_process(self, opportunity: Opportunity, initiated_by: str) -> Dict[str, Any]:
        """Start the matching process for a submitted opportunity."""
        self.logger.info(f"Starting matching process for opportunity {opportunity.id}")
        
        if opportunity.status != OpportunityStatus.SUBMITTED:
            return {
                "success": False,
                "errors": ["Only submitted opportunities can enter matching process"],
                "status": opportunity.status.value
            }
        
        try:
            opportunity.change_status(
                new_status=OpportunityStatus.MATCHING_IN_PROGRESS,
                changed_by=initiated_by,
                reason="Matching process initiated",
                notes="Searching for suitable Solution Architects"
            )
            
            self.logger.info(f"Matching process started for opportunity {opportunity.id}")
            
            return {
                "success": True,
                "message": "Matching process started",
                "status": opportunity.status.value,
                "estimated_completion": "2-3 business days"
            }
            
        except Exception as e:
            self.logger.error(f"Error starting matching for opportunity {opportunity.id}: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "status": opportunity.status.value
            }
    
    def complete_matching_process(self, opportunity: Opportunity, matches_found: bool, 
                                completed_by: str, match_count: int = 0) -> Dict[str, Any]:
        """Complete the matching process with results."""
        self.logger.info(f"Completing matching process for opportunity {opportunity.id}")
        
        if opportunity.status != OpportunityStatus.MATCHING_IN_PROGRESS:
            return {
                "success": False,
                "errors": ["Matching process is not in progress"],
                "status": opportunity.status.value
            }
        
        try:
            if matches_found and match_count > 0:
                opportunity.change_status(
                    new_status=OpportunityStatus.MATCHES_FOUND,
                    changed_by=completed_by,
                    reason="Matching process completed successfully",
                    notes=f"Found {match_count} suitable Solution Architect(s)"
                )
                
                return {
                    "success": True,
                    "message": f"Matching completed - {match_count} architects found",
                    "status": opportunity.status.value,
                    "next_steps": ["Review architect profiles", "Select preferred architect"]
                }
            else:
                # No matches found - opportunity goes back to submitted for review
                opportunity.change_status(
                    new_status=OpportunityStatus.SUBMITTED,
                    changed_by=completed_by,
                    reason="No suitable matches found",
                    notes="Consider adjusting requirements or timeline"
                )
                
                return {
                    "success": True,
                    "message": "No matches found - opportunity returned for review",
                    "status": opportunity.status.value,
                    "recommendations": [
                        "Consider making some skills 'Nice to Have'",
                        "Review timeline flexibility",
                        "Expand geographic requirements"
                    ]
                }
                
        except Exception as e:
            self.logger.error(f"Error completing matching for opportunity {opportunity.id}: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "status": opportunity.status.value
            }
    
    def select_architect(self, opportunity: Opportunity, architect_id: str, 
                        selected_by: str, selection_notes: Optional[str] = None) -> Dict[str, Any]:
        """Select a solution architect for the opportunity."""
        self.logger.info(f"Selecting architect {architect_id} for opportunity {opportunity.id}")
        
        # Validate architect selection
        validation_errors = self.validation_service.validate_architect_selection(opportunity, architect_id)
        if validation_errors:
            return {
                "success": False,
                "errors": validation_errors,
                "status": opportunity.status.value
            }
        
        try:
            opportunity.select_architect(architect_id, selected_by)
            
            # Add additional notes if provided
            if selection_notes:
                latest_history = opportunity.status_history[-1]
                latest_history.notes = f"{latest_history.notes}. {selection_notes}"
            
            self.logger.info(f"Architect {architect_id} selected for opportunity {opportunity.id}")
            
            return {
                "success": True,
                "message": "Solution Architect selected successfully",
                "status": opportunity.status.value,
                "selected_architect_id": architect_id,
                "next_steps": ["Architect will be notified", "Project kickoff can be scheduled"]
            }
            
        except Exception as e:
            self.logger.error(f"Error selecting architect for opportunity {opportunity.id}: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "status": opportunity.status.value
            }
    
    def complete_opportunity(self, opportunity: Opportunity, completed_by: str, 
                           completion_notes: Optional[str] = None) -> Dict[str, Any]:
        """Mark opportunity as completed."""
        self.logger.info(f"Completing opportunity {opportunity.id}")
        
        # Validate completion
        validation_errors = self.validation_service.validate_completion(opportunity)
        if validation_errors:
            return {
                "success": False,
                "errors": validation_errors,
                "status": opportunity.status.value
            }
        
        try:
            opportunity.complete_opportunity(completed_by, completion_notes)
            
            self.logger.info(f"Opportunity {opportunity.id} completed successfully")
            
            return {
                "success": True,
                "message": "Opportunity completed successfully",
                "status": opportunity.status.value,
                "completion_date": opportunity.completion_date.isoformat() if opportunity.completion_date else None,
                "final_notes": completion_notes
            }
            
        except Exception as e:
            self.logger.error(f"Error completing opportunity {opportunity.id}: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "status": opportunity.status.value
            }
    
    def cancel_opportunity(self, opportunity: Opportunity, cancelled_by: str, 
                          reason: str, notes: Optional[str] = None) -> Dict[str, Any]:
        """Cancel an opportunity."""
        self.logger.info(f"Cancelling opportunity {opportunity.id}")
        
        # Validate cancellation
        validation_errors = self.validation_service.validate_cancellation(opportunity, reason)
        if validation_errors:
            return {
                "success": False,
                "errors": validation_errors,
                "status": opportunity.status.value
            }
        
        try:
            opportunity.cancel_opportunity(cancelled_by, reason, notes)
            
            self.logger.info(f"Opportunity {opportunity.id} cancelled: {reason}")
            
            return {
                "success": True,
                "message": "Opportunity cancelled successfully",
                "status": opportunity.status.value,
                "cancellation_date": opportunity.cancellation_date.isoformat() if opportunity.cancellation_date else None,
                "cancellation_reason": reason,
                "reactivation_deadline": self._calculate_reactivation_deadline(opportunity.cancellation_date)
            }
            
        except Exception as e:
            self.logger.error(f"Error cancelling opportunity {opportunity.id}: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "status": opportunity.status.value
            }
    
    def reactivate_opportunity(self, opportunity: Opportunity, reactivated_by: str, 
                             notes: Optional[str] = None) -> Dict[str, Any]:
        """Reactivate a cancelled opportunity."""
        self.logger.info(f"Reactivating opportunity {opportunity.id}")
        
        # Validate reactivation
        validation_errors = self.validation_service.validate_reactivation(opportunity)
        if validation_errors:
            return {
                "success": False,
                "errors": validation_errors,
                "status": opportunity.status.value
            }
        
        try:
            opportunity.reactivate_opportunity(reactivated_by, notes)
            
            self.logger.info(f"Opportunity {opportunity.id} reactivated successfully")
            
            return {
                "success": True,
                "message": "Opportunity reactivated successfully",
                "status": opportunity.status.value,
                "next_steps": ["Review and update requirements if needed", "Resubmit when ready"]
            }
            
        except Exception as e:
            self.logger.error(f"Error reactivating opportunity {opportunity.id}: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "status": opportunity.status.value
            }
    
    def get_available_transitions(self, opportunity: Opportunity) -> List[Dict[str, Any]]:
        """Get available status transitions for an opportunity."""
        current_status = opportunity.status
        available_transitions = []
        
        for status in OpportunityStatus:
            if current_status.can_transition_to(status):
                transition_info = {
                    "to_status": status.value,
                    "description": self._get_transition_description(current_status, status),
                    "requires_validation": self._requires_validation(current_status, status)
                }
                available_transitions.append(transition_info)
        
        return available_transitions
    
    def _get_transition_description(self, from_status: OpportunityStatus, 
                                  to_status: OpportunityStatus) -> str:
        """Get description for status transition."""
        descriptions = {
            (OpportunityStatus.DRAFT, OpportunityStatus.SUBMITTED): "Submit for matching",
            (OpportunityStatus.SUBMITTED, OpportunityStatus.MATCHING_IN_PROGRESS): "Start matching process",
            (OpportunityStatus.MATCHING_IN_PROGRESS, OpportunityStatus.MATCHES_FOUND): "Complete matching with results",
            (OpportunityStatus.MATCHES_FOUND, OpportunityStatus.ARCHITECT_SELECTED): "Select solution architect",
            (OpportunityStatus.ARCHITECT_SELECTED, OpportunityStatus.COMPLETED): "Mark as completed",
            (OpportunityStatus.CANCELLED, OpportunityStatus.DRAFT): "Reactivate opportunity"
        }
        
        return descriptions.get((from_status, to_status), f"Change to {to_status.value}")
    
    def _requires_validation(self, from_status: OpportunityStatus, 
                           to_status: OpportunityStatus) -> bool:
        """Check if transition requires special validation."""
        validation_required = [
            (OpportunityStatus.DRAFT, OpportunityStatus.SUBMITTED),
            (OpportunityStatus.MATCHES_FOUND, OpportunityStatus.ARCHITECT_SELECTED),
            (OpportunityStatus.CANCELLED, OpportunityStatus.DRAFT)
        ]
        
        return (from_status, to_status) in validation_required
    
    def _calculate_reactivation_deadline(self, cancellation_date: Optional[date]) -> Optional[str]:
        """Calculate the deadline for reactivating a cancelled opportunity."""
        if not cancellation_date:
            return None
        
        from datetime import timedelta
        deadline = cancellation_date + timedelta(days=90)
        return deadline.isoformat()
