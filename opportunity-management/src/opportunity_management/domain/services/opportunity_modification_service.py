"""
Opportunity modification service for handling opportunity updates with business rules.
"""

from typing import List, Dict, Any, Optional
from decimal import Decimal
import logging

from ..entities.opportunity import Opportunity
from ..enums.status import OpportunityStatus
from ..enums.priority import Priority
from ..value_objects.skill_requirement import SkillRequirement
from ..value_objects.timeline_specification import TimelineSpecification
from .opportunity_validation_service import OpportunityValidationService


class OpportunityModificationService:
    """Service for handling opportunity modifications with proper business rules."""
    
    def __init__(self, validation_service: OpportunityValidationService):
        """Initialize the modification service."""
        self.validation_service = validation_service
        self.logger = logging.getLogger(__name__)
    
    def update_basic_information(self, opportunity: Opportunity, 
                               modification_data: Dict[str, Any],
                               modified_by: str) -> Dict[str, Any]:
        """Update basic opportunity information with validation."""
        self.logger.info(f"Updating basic information for opportunity {opportunity.id}")
        
        # Validate modification permissions
        validation_errors = self.validation_service.validate_for_modification(
            opportunity, modification_data
        )
        if validation_errors:
            return {
                "success": False,
                "errors": validation_errors,
                "current_status": opportunity.status.value
            }
        
        try:
            changes_made = []
            
            # Update title
            if 'title' in modification_data:
                old_title = opportunity.title
                opportunity.update_basic_info(title=modification_data['title'])
                changes_made.append(f"Title changed from '{old_title}' to '{opportunity.title}'")
            
            # Update description
            if 'description' in modification_data:
                opportunity.update_basic_info(description=modification_data['description'])
                changes_made.append("Description updated")
            
            # Update ARR
            if 'annual_recurring_revenue' in modification_data:
                old_arr = opportunity.annual_recurring_revenue
                new_arr = Decimal(str(modification_data['annual_recurring_revenue']))
                opportunity.update_basic_info(annual_recurring_revenue=new_arr)
                changes_made.append(f"ARR changed from ${old_arr} to ${new_arr}")
            
            # Update priority
            if 'priority' in modification_data:
                old_priority = opportunity.priority
                new_priority = Priority.from_string(modification_data['priority'])
                opportunity.update_basic_info(priority=new_priority)
                changes_made.append(f"Priority changed from {old_priority} to {new_priority}")
            
            self.logger.info(f"Basic information updated for opportunity {opportunity.id}")
            
            return {
                "success": True,
                "message": "Basic information updated successfully",
                "changes_made": changes_made,
                "modified_by": modified_by,
                "modification_timestamp": opportunity.updated_at.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error updating opportunity {opportunity.id}: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "current_status": opportunity.status.value
            }
    
    def update_skill_requirements(self, opportunity: Opportunity,
                                skill_updates: Dict[str, Any],
                                modified_by: str) -> Dict[str, Any]:
        """Update skill requirements for an opportunity."""
        self.logger.info(f"Updating skill requirements for opportunity {opportunity.id}")
        
        if not opportunity.status.is_modifiable:
            return {
                "success": False,
                "errors": [f"Cannot modify skills in {opportunity.status} status"],
                "current_status": opportunity.status.value
            }
        
        try:
            changes_made = []
            
            # Add new skills
            if 'add_skills' in skill_updates:
                for skill_data in skill_updates['add_skills']:
                    skill_requirement = SkillRequirement.from_dict(skill_data)
                    opportunity.add_skill_requirement(skill_requirement)
                    changes_made.append(f"Added skill: {skill_requirement.skill_name}")
            
            # Remove skills
            if 'remove_skills' in skill_updates:
                for skill_info in skill_updates['remove_skills']:
                    skill_name = skill_info['skill_name']
                    skill_category = skill_info['skill_category']
                    if opportunity.remove_skill_requirement(skill_name, skill_category):
                        changes_made.append(f"Removed skill: {skill_name}")
                    else:
                        changes_made.append(f"Skill not found: {skill_name}")
            
            # Validate final skill set
            from skills_validation_service import SkillsValidationService
            skills_validator = SkillsValidationService()
            validation_errors = skills_validator.validate_skill_requirements_collection(
                opportunity.skill_requirements
            )
            
            if validation_errors:
                return {
                    "success": False,
                    "errors": validation_errors,
                    "current_status": opportunity.status.value
                }
            
            self.logger.info(f"Skill requirements updated for opportunity {opportunity.id}")
            
            return {
                "success": True,
                "message": "Skill requirements updated successfully",
                "changes_made": changes_made,
                "total_skills": len(opportunity.skill_requirements),
                "mandatory_skills": len(opportunity.mandatory_skills)
            }
            
        except Exception as e:
            self.logger.error(f"Error updating skills for opportunity {opportunity.id}: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "current_status": opportunity.status.value
            }
    
    def update_timeline(self, opportunity: Opportunity,
                       timeline_data: Dict[str, Any],
                       modified_by: str) -> Dict[str, Any]:
        """Update timeline specification for an opportunity."""
        self.logger.info(f"Updating timeline for opportunity {opportunity.id}")
        
        # Check modification permissions based on status
        if opportunity.status == OpportunityStatus.ARCHITECT_SELECTED:
            if (opportunity.timeline_specification and 
                not opportunity.timeline_specification.flexibility.allows_adjustment):
                return {
                    "success": False,
                    "errors": ["Timeline cannot be modified for fixed timelines after architect selection"],
                    "current_status": opportunity.status.value
                }
        elif not opportunity.status.is_modifiable:
            return {
                "success": False,
                "errors": [f"Cannot modify timeline in {opportunity.status} status"],
                "current_status": opportunity.status.value
            }
        
        try:
            # Validate timeline data
            from timeline_validation_service import TimelineValidationService
            timeline_validator = TimelineValidationService()
            
            validation_errors = timeline_validator.validate_timeline_specification(timeline_data)
            if validation_errors:
                return {
                    "success": False,
                    "errors": validation_errors,
                    "current_status": opportunity.status.value
                }
            
            # Additional validation for modifications
            if opportunity.timeline_specification:
                modification_errors = timeline_validator.validate_timeline_modification(
                    opportunity.timeline_specification,
                    timeline_data,
                    opportunity.status.value
                )
                if modification_errors:
                    return {
                        "success": False,
                        "errors": modification_errors,
                        "current_status": opportunity.status.value
                    }
            
            # Create new timeline specification
            new_timeline = TimelineSpecification.from_dict(timeline_data)
            old_timeline = opportunity.timeline_specification
            
            opportunity.set_timeline_specification(new_timeline)
            
            # Track changes
            changes_made = []
            if old_timeline:
                if old_timeline.expected_start_date != new_timeline.expected_start_date:
                    changes_made.append(f"Start date changed from {old_timeline.expected_start_date} to {new_timeline.expected_start_date}")
                if old_timeline.expected_duration_days != new_timeline.expected_duration_days:
                    changes_made.append(f"Duration changed from {old_timeline.expected_duration_days} to {new_timeline.expected_duration_days} days")
                if old_timeline.flexibility != new_timeline.flexibility:
                    changes_made.append(f"Flexibility changed from {old_timeline.flexibility} to {new_timeline.flexibility}")
            else:
                changes_made.append("Timeline specification added")
            
            self.logger.info(f"Timeline updated for opportunity {opportunity.id}")
            
            return {
                "success": True,
                "message": "Timeline updated successfully",
                "changes_made": changes_made,
                "new_timeline": new_timeline.to_dict()
            }
            
        except Exception as e:
            self.logger.error(f"Error updating timeline for opportunity {opportunity.id}: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "current_status": opportunity.status.value
            }
    
    def update_problem_statement(self, opportunity: Opportunity,
                               problem_statement_data: Dict[str, Any],
                               modified_by: str) -> Dict[str, Any]:
        """Update problem statement for an opportunity."""
        self.logger.info(f"Updating problem statement for opportunity {opportunity.id}")
        
        if not opportunity.status.is_modifiable:
            return {
                "success": False,
                "errors": [f"Cannot modify problem statement in {opportunity.status} status"],
                "current_status": opportunity.status.value
            }
        
        try:
            changes_made = []
            
            if opportunity.problem_statement:
                # Update existing problem statement
                if 'title' in problem_statement_data:
                    opportunity.problem_statement.title = problem_statement_data['title']
                    changes_made.append("Title updated")
                
                if 'description' in problem_statement_data:
                    opportunity.problem_statement.update_description(problem_statement_data['description'])
                    changes_made.append("Description updated")
                
                if 'business_impact' in problem_statement_data:
                    opportunity.problem_statement.update_business_impact(problem_statement_data['business_impact'])
                    changes_made.append("Business impact updated")
                
                if 'technical_requirements' in problem_statement_data:
                    opportunity.problem_statement.update_technical_requirements(problem_statement_data['technical_requirements'])
                    changes_made.append("Technical requirements updated")
                
                if 'success_criteria' in problem_statement_data:
                    opportunity.problem_statement.update_success_criteria(problem_statement_data['success_criteria'])
                    changes_made.append("Success criteria updated")
                
                if 'constraints' in problem_statement_data:
                    opportunity.problem_statement.update_constraints(problem_statement_data['constraints'])
                    changes_made.append("Constraints updated")
            else:
                # Create new problem statement
                from problem_statement import ProblemStatement
                problem_statement = ProblemStatement(
                    title=problem_statement_data['title'],
                    description=problem_statement_data['description'],
                    business_impact=problem_statement_data.get('business_impact'),
                    technical_requirements=problem_statement_data.get('technical_requirements'),
                    success_criteria=problem_statement_data.get('success_criteria'),
                    constraints=problem_statement_data.get('constraints')
                )
                opportunity.set_problem_statement(problem_statement)
                changes_made.append("Problem statement created")
            
            self.logger.info(f"Problem statement updated for opportunity {opportunity.id}")
            
            return {
                "success": True,
                "message": "Problem statement updated successfully",
                "changes_made": changes_made,
                "is_complete": opportunity.problem_statement.is_complete if opportunity.problem_statement else False
            }
            
        except Exception as e:
            self.logger.error(f"Error updating problem statement for opportunity {opportunity.id}: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)],
                "current_status": opportunity.status.value
            }
    
    def get_modification_permissions(self, opportunity: Opportunity) -> Dict[str, Any]:
        """Get what can be modified for an opportunity based on its current status."""
        permissions = {
            "can_modify_basic_info": False,
            "can_modify_skills": False,
            "can_modify_timeline": False,
            "can_modify_problem_statement": False,
            "can_add_attachments": False,
            "modifiable_fields": [],
            "restrictions": []
        }
        
        if opportunity.status.is_modifiable:
            # Full modification allowed
            permissions.update({
                "can_modify_basic_info": True,
                "can_modify_skills": True,
                "can_modify_timeline": True,
                "can_modify_problem_statement": True,
                "can_add_attachments": True,
                "modifiable_fields": ["title", "description", "priority", "arr", "skills", "timeline", "problem_statement"]
            })
        elif opportunity.status == OpportunityStatus.ARCHITECT_SELECTED:
            # Limited modifications allowed
            permissions.update({
                "can_modify_basic_info": True,
                "modifiable_fields": ["priority", "notes"],
                "restrictions": ["Only priority and notes can be modified after architect selection"]
            })
            
            # Timeline modification depends on flexibility
            if (opportunity.timeline_specification and 
                opportunity.timeline_specification.flexibility.allows_adjustment):
                permissions["can_modify_timeline"] = True
                permissions["modifiable_fields"].append("timeline")
        else:
            permissions["restrictions"].append(f"No modifications allowed in {opportunity.status} status")
        
        return permissions
    
    def create_modification_audit_log(self, opportunity: Opportunity, 
                                    changes: List[str], modified_by: str) -> Dict[str, Any]:
        """Create an audit log entry for opportunity modifications."""
        return {
            "opportunity_id": opportunity.id,
            "modified_by": modified_by,
            "modification_timestamp": opportunity.updated_at.isoformat(),
            "opportunity_version": opportunity.version,
            "changes_made": changes,
            "status_at_modification": opportunity.status.value
        }
