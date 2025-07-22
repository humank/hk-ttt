"""
Opportunity application service for orchestrating use cases and business workflows.
"""

from typing import Dict, Any, List, Optional
from decimal import Decimal
import logging

from ...domain.entities.opportunity import Opportunity
from ...domain.entities.customer import Customer
from ...domain.entities.problem_statement import ProblemStatement
from ...domain.value_objects.skill_requirement import SkillRequirement
from ...domain.value_objects.timeline_specification import TimelineSpecification
from ...domain.value_objects.geographic_requirement import GeographicRequirement
from ...domain.value_objects.language_requirement import LanguageRequirements
from ...domain.enums.priority import Priority
from ...domain.enums.status import OpportunityStatus

from ...infrastructure.repositories.opportunity_repository import OpportunityRepository
from ...infrastructure.repositories.customer_repository import CustomerRepository
from ...domain.services.opportunity_validation_service import OpportunityValidationService
from ...domain.services.status_transition_service import StatusTransitionService
from ...domain.services.opportunity_modification_service import OpportunityModificationService
from ...domain.services.skills_matching_preparation_service import SkillsMatchingPreparationService
from ...infrastructure.event_handling.event_dispatcher import get_event_dispatcher

from opportunity_created_event import OpportunityCreatedEvent
from opportunity_modified_event import OpportunityModifiedEvent
from status_changed_event import StatusChangedEvent


class OpportunityApplicationService:
    """Application service for orchestrating opportunity-related use cases."""
    
    def __init__(self, 
                 opportunity_repository: OpportunityRepository,
                 customer_repository: CustomerRepository,
                 validation_service: OpportunityValidationService,
                 status_transition_service: StatusTransitionService,
                 modification_service: OpportunityModificationService,
                 matching_preparation_service: SkillsMatchingPreparationService):
        """Initialize the application service with dependencies."""
        self.opportunity_repository = opportunity_repository
        self.customer_repository = customer_repository
        self.validation_service = validation_service
        self.status_transition_service = status_transition_service
        self.modification_service = modification_service
        self.matching_preparation_service = matching_preparation_service
        self.event_dispatcher = get_event_dispatcher()
        self.logger = logging.getLogger(__name__)
    
    def create_opportunity(self, opportunity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new opportunity (US-SM-3: Customer Opportunity Creation)."""
        self.logger.info("Creating new opportunity")
        
        try:
            # Validate opportunity data
            validation_errors = self.validation_service.validate_for_creation(opportunity_data)
            if validation_errors:
                return {
                    "success": False,
                    "errors": validation_errors
                }
            
            # Verify customer exists or create new one
            customer_id = opportunity_data.get('customer_id')
            customer_name = opportunity_data.get('customer_name')
            
            if customer_id:
                customer = self.customer_repository.find_by_id(customer_id)
                if not customer:
                    return {
                        "success": False,
                        "errors": ["Customer not found"]
                    }
            elif customer_name:
                # Create new customer
                customer = Customer(name=customer_name)
                customer = self.customer_repository.save(customer)
                customer_id = customer.id
            else:
                return {
                    "success": False,
                    "errors": ["Either customer_id or customer_name must be provided"]
                }
            
            # Create opportunity
            opportunity = Opportunity(
                title=opportunity_data['title'],
                description=opportunity_data['description'],
                customer_id=customer_id,
                sales_manager_id=opportunity_data['sales_manager_id'],
                annual_recurring_revenue=Decimal(str(opportunity_data['annual_recurring_revenue'])),
                priority=Priority.from_string(opportunity_data['priority'])
            )
            
            # Save opportunity
            opportunity = self.opportunity_repository.save(opportunity)
            
            # Raise domain event
            event = OpportunityCreatedEvent.create(
                opportunity_id=opportunity.id,
                opportunity_title=opportunity.title,
                customer_id=customer_id,
                sales_manager_id=opportunity.sales_manager_id,
                annual_recurring_revenue=opportunity.annual_recurring_revenue,
                priority=opportunity.priority.value,
                user_id=opportunity.sales_manager_id
            )
            self.event_dispatcher.dispatch(event)
            
            self.logger.info(f"Opportunity {opportunity.id} created successfully")
            
            return {
                "success": True,
                "opportunity_id": opportunity.id,
                "message": "Opportunity created successfully",
                "opportunity": opportunity.to_dict()
            }
            
        except Exception as e:
            self.logger.error(f"Error creating opportunity: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)]
            }
    
    def add_problem_statement(self, opportunity_id: str, problem_data: Dict[str, Any],
                            user_id: str) -> Dict[str, Any]:
        """Add problem statement to opportunity (US-SM-4: Problem Statement Documentation)."""
        self.logger.info(f"Adding problem statement to opportunity {opportunity_id}")
        
        try:
            opportunity = self.opportunity_repository.find_by_id(opportunity_id)
            if not opportunity:
                return {
                    "success": False,
                    "errors": ["Opportunity not found"]
                }
            
            # Create problem statement
            problem_statement = ProblemStatement(
                title=problem_data['title'],
                description=problem_data['description'],
                business_impact=problem_data.get('business_impact'),
                technical_requirements=problem_data.get('technical_requirements'),
                success_criteria=problem_data.get('success_criteria'),
                constraints=problem_data.get('constraints')
            )
            
            opportunity.set_problem_statement(problem_statement)
            self.opportunity_repository.save(opportunity)
            
            self.logger.info(f"Problem statement added to opportunity {opportunity_id}")
            
            return {
                "success": True,
                "message": "Problem statement added successfully",
                "is_complete": problem_statement.is_complete
            }
            
        except Exception as e:
            self.logger.error(f"Error adding problem statement: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)]
            }
    
    def add_skill_requirements(self, opportunity_id: str, skills_data: List[Dict[str, Any]],
                             user_id: str) -> Dict[str, Any]:
        """Add skill requirements to opportunity (US-SM-5: Required Skills Specification)."""
        self.logger.info(f"Adding skill requirements to opportunity {opportunity_id}")
        
        try:
            opportunity = self.opportunity_repository.find_by_id(opportunity_id)
            if not opportunity:
                return {
                    "success": False,
                    "errors": ["Opportunity not found"]
                }
            
            # Create skill requirements
            skill_requirements = []
            for skill_data in skills_data:
                skill_req = SkillRequirement.from_dict(skill_data)
                skill_requirements.append(skill_req)
            
            # Add skills to opportunity
            for skill_req in skill_requirements:
                opportunity.add_skill_requirement(skill_req)
            
            self.opportunity_repository.save(opportunity)
            
            self.logger.info(f"Added {len(skill_requirements)} skill requirements to opportunity {opportunity_id}")
            
            return {
                "success": True,
                "message": f"Added {len(skill_requirements)} skill requirements",
                "total_skills": len(opportunity.skill_requirements),
                "mandatory_skills": len(opportunity.mandatory_skills)
            }
            
        except Exception as e:
            self.logger.error(f"Error adding skill requirements: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)]
            }
    
    def set_timeline(self, opportunity_id: str, timeline_data: Dict[str, Any],
                    user_id: str) -> Dict[str, Any]:
        """Set timeline for opportunity (US-SM-6: Opportunity Timeline Management)."""
        self.logger.info(f"Setting timeline for opportunity {opportunity_id}")
        
        try:
            opportunity = self.opportunity_repository.find_by_id(opportunity_id)
            if not opportunity:
                return {
                    "success": False,
                    "errors": ["Opportunity not found"]
                }
            
            # Create timeline specification
            timeline_spec = TimelineSpecification.from_dict(timeline_data)
            opportunity.set_timeline_specification(timeline_spec)
            
            self.opportunity_repository.save(opportunity)
            
            self.logger.info(f"Timeline set for opportunity {opportunity_id}")
            
            return {
                "success": True,
                "message": "Timeline set successfully",
                "timeline": timeline_spec.to_dict()
            }
            
        except Exception as e:
            self.logger.error(f"Error setting timeline: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)]
            }
    
    def submit_opportunity(self, opportunity_id: str, user_id: str) -> Dict[str, Any]:
        """Submit opportunity for matching."""
        self.logger.info(f"Submitting opportunity {opportunity_id}")
        
        try:
            opportunity = self.opportunity_repository.find_by_id(opportunity_id)
            if not opportunity:
                return {
                    "success": False,
                    "errors": ["Opportunity not found"]
                }
            
            # Use status transition service
            result = self.status_transition_service.submit_opportunity(opportunity, user_id)
            
            if result["success"]:
                self.opportunity_repository.save(opportunity)
                
                # Dispatch events
                for event in opportunity.get_domain_events():
                    self.event_dispatcher.dispatch(event)
                opportunity.clear_domain_events()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error submitting opportunity: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)]
            }
    
    def modify_opportunity(self, opportunity_id: str, modification_data: Dict[str, Any],
                          user_id: str) -> Dict[str, Any]:
        """Modify opportunity details (US-SM-8: Opportunity Modification)."""
        self.logger.info(f"Modifying opportunity {opportunity_id}")
        
        try:
            opportunity = self.opportunity_repository.find_by_id(opportunity_id)
            if not opportunity:
                return {
                    "success": False,
                    "errors": ["Opportunity not found"]
                }
            
            # Store previous values for event
            previous_values = {}
            if 'title' in modification_data:
                previous_values['title'] = opportunity.title
            if 'priority' in modification_data:
                previous_values['priority'] = opportunity.priority.value
            
            # Use modification service
            result = self.modification_service.update_basic_information(
                opportunity, modification_data, user_id
            )
            
            if result["success"]:
                self.opportunity_repository.save(opportunity)
                
                # Raise modification event
                event = OpportunityModifiedEvent.create(
                    opportunity_id=opportunity.id,
                    opportunity_title=opportunity.title,
                    modified_fields=list(modification_data.keys()),
                    changes_summary=result.get("changes_made", []),
                    previous_values=previous_values,
                    new_values=modification_data,
                    opportunity_status=opportunity.status.value,
                    user_id=user_id
                )
                self.event_dispatcher.dispatch(event)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error modifying opportunity: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)]
            }
    
    def cancel_opportunity(self, opportunity_id: str, reason: str, 
                          user_id: str, notes: Optional[str] = None) -> Dict[str, Any]:
        """Cancel opportunity (US-SM-9: Opportunity Cancellation)."""
        self.logger.info(f"Cancelling opportunity {opportunity_id}")
        
        try:
            opportunity = self.opportunity_repository.find_by_id(opportunity_id)
            if not opportunity:
                return {
                    "success": False,
                    "errors": ["Opportunity not found"]
                }
            
            # Use status transition service
            result = self.status_transition_service.cancel_opportunity(
                opportunity, user_id, reason, notes
            )
            
            if result["success"]:
                self.opportunity_repository.save(opportunity)
                
                # Dispatch events
                for event in opportunity.get_domain_events():
                    self.event_dispatcher.dispatch(event)
                opportunity.clear_domain_events()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error cancelling opportunity: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)]
            }
    
    def reactivate_opportunity(self, opportunity_id: str, user_id: str,
                             notes: Optional[str] = None) -> Dict[str, Any]:
        """Reactivate cancelled opportunity."""
        self.logger.info(f"Reactivating opportunity {opportunity_id}")
        
        try:
            opportunity = self.opportunity_repository.find_by_id(opportunity_id)
            if not opportunity:
                return {
                    "success": False,
                    "errors": ["Opportunity not found"]
                }
            
            # Use status transition service
            result = self.status_transition_service.reactivate_opportunity(
                opportunity, user_id, notes
            )
            
            if result["success"]:
                self.opportunity_repository.save(opportunity)
                
                # Dispatch events
                for event in opportunity.get_domain_events():
                    self.event_dispatcher.dispatch(event)
                opportunity.clear_domain_events()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error reactivating opportunity: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)]
            }
    
    def clone_opportunity(self, opportunity_id: str, new_title: str, 
                         user_id: str) -> Dict[str, Any]:
        """Clone an existing opportunity."""
        self.logger.info(f"Cloning opportunity {opportunity_id}")
        
        try:
            original_opportunity = self.opportunity_repository.find_by_id(opportunity_id)
            if not original_opportunity:
                return {
                    "success": False,
                    "errors": ["Original opportunity not found"]
                }
            
            # Clone the opportunity
            cloned_opportunity = original_opportunity.clone_opportunity(new_title, user_id)
            cloned_opportunity = self.opportunity_repository.save(cloned_opportunity)
            
            # Raise creation event for cloned opportunity
            event = OpportunityCreatedEvent.create(
                opportunity_id=cloned_opportunity.id,
                opportunity_title=cloned_opportunity.title,
                customer_id=cloned_opportunity.customer_id,
                sales_manager_id=cloned_opportunity.sales_manager_id,
                annual_recurring_revenue=cloned_opportunity.annual_recurring_revenue,
                priority=cloned_opportunity.priority.value,
                user_id=user_id
            )
            self.event_dispatcher.dispatch(event)
            
            self.logger.info(f"Opportunity {opportunity_id} cloned as {cloned_opportunity.id}")
            
            return {
                "success": True,
                "message": "Opportunity cloned successfully",
                "original_id": opportunity_id,
                "cloned_id": cloned_opportunity.id,
                "cloned_opportunity": cloned_opportunity.to_dict()
            }
            
        except Exception as e:
            self.logger.error(f"Error cloning opportunity: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)]
            }
    
    def prepare_for_matching(self, opportunity_id: str) -> Dict[str, Any]:
        """Prepare opportunity for matching process."""
        self.logger.info(f"Preparing opportunity {opportunity_id} for matching")
        
        try:
            opportunity = self.opportunity_repository.find_by_id(opportunity_id)
            if not opportunity:
                return {
                    "success": False,
                    "errors": ["Opportunity not found"]
                }
            
            # Validate readiness
            readiness = self.matching_preparation_service.validate_matching_readiness(opportunity)
            if not readiness["is_ready"]:
                return {
                    "success": False,
                    "errors": readiness["issues"],
                    "warnings": readiness["warnings"]
                }
            
            # Prepare matching criteria
            matching_criteria = self.matching_preparation_service.prepare_matching_criteria(opportunity)
            
            return {
                "success": True,
                "message": "Opportunity prepared for matching",
                "matching_criteria": matching_criteria,
                "readiness_score": readiness["readiness_score"]
            }
            
        except Exception as e:
            self.logger.error(f"Error preparing for matching: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)]
            }
