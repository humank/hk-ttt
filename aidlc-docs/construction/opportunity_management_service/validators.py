"""
Validators for the Opportunity Management Service.
"""

import uuid
from typing import List, Optional, Dict, Any
import logging

from .common import ValidationException, NotFoundException

logger = logging.getLogger(__name__)

class OpportunityValidator:
    """Validator for Opportunity entities."""
    
    @staticmethod
    def validate_required_fields(title: str, description: str, customer_id: uuid.UUID,
                               customer_name: str, sales_manager_id: uuid.UUID,
                               priority: Any, annual_recurring_revenue: float,
                               geographic_requirements: Any) -> None:
        """Validate required fields for opportunity creation."""
        if not title:
            raise ValidationException("Title is required")
        
        if not description:
            raise ValidationException("Description is required")
        
        if not customer_id:
            raise ValidationException("Customer ID is required")
        
        if not customer_name:
            raise ValidationException("Customer name is required")
        
        if not sales_manager_id:
            raise ValidationException("Sales Manager ID is required")
        
        if not priority:
            raise ValidationException("Priority is required")
        
        if annual_recurring_revenue is None or annual_recurring_revenue < 0:
            raise ValidationException("Annual Recurring Revenue must be a non-negative value")
        
        if not geographic_requirements:
            raise ValidationException("Geographic requirements are required")
        
        logger.info("Opportunity required fields validated successfully")

class ProblemStatementValidator:
    """Validator for ProblemStatement entities."""
    
    @staticmethod
    def validate_content(content: str, minimum_character_count: int = 140) -> None:
        """Validate problem statement content."""
        if not content:
            raise ValidationException("Problem statement content is required")
        
        if len(content) < minimum_character_count:
            raise ValidationException(
                f"Problem statement must be at least {minimum_character_count} characters long"
            )
        
        logger.info("Problem statement content validated successfully")

class SkillRequirementValidator:
    """Validator for SkillRequirement entities."""
    
    @staticmethod
    def validate_skill_requirements(skill_requirements: List[Any]) -> None:
        """Validate skill requirements."""
        if not skill_requirements:
            raise ValidationException("At least one skill requirement is required")
        
        # Check if at least one "Must Have" skill is specified
        must_have_skills = [sr for sr in skill_requirements if sr.importance_level.value == "Must Have"]
        if not must_have_skills:
            raise ValidationException("At least one 'Must Have' skill is required")
        
        logger.info("Skill requirements validated successfully")
    
    @staticmethod
    def validate_skill_exists(skill_id: uuid.UUID, skills_catalog_repository) -> None:
        """Validate that a skill exists in the Skills Catalog."""
        skill = skills_catalog_repository.get_by_id(skill_id)
        if not skill:
            raise NotFoundException(f"Skill with ID {skill_id} not found in Skills Catalog")
        
        if not skill.is_active:
            raise ValidationException(f"Skill with ID {skill_id} is not active")
        
        logger.info(f"Skill {skill_id} validated successfully")

class TimelineValidator:
    """Validator for TimelineRequirement entities."""
    
    @staticmethod
    def validate_timeline(start_date: str, end_date: str, specific_days: Optional[List[str]] = None) -> None:
        """Validate timeline information."""
        from datetime import datetime
        from dateutil.parser import parse
        
        try:
            start = parse(start_date).date()
            end = parse(end_date).date()
            
            if end <= start:
                raise ValidationException("End date must be after start date")
            
            if specific_days:
                for day_str in specific_days:
                    day = parse(day_str).date()
                    if day < start or day > end:
                        raise ValidationException(
                            f"Specific required day {day_str} is outside the timeline range"
                        )
            
            logger.info("Timeline validated successfully")
            
        except ValueError as e:
            raise ValidationException(f"Invalid date format: {str(e)}")

class AttachmentValidator:
    """Validator for Attachment entities."""
    
    @staticmethod
    def validate_attachment(file_name: str, file_type: str, file_size: int) -> None:
        """Validate attachment information."""
        if not file_name:
            raise ValidationException("File name is required")
        
        if not file_type:
            raise ValidationException("File type is required")
        
        # Validate file size (20MB limit as per clarification)
        max_size = 20 * 1024 * 1024  # 20MB in bytes
        if file_size > max_size:
            raise ValidationException(f"File size exceeds the maximum allowed size of 20MB")
        
        logger.info("Attachment validated successfully")

class StatusTransitionValidator:
    """Validator for status transitions."""
    
    @staticmethod
    def validate_transition(current_status: Any, new_status: Any) -> None:
        """Validate status transition."""
        from .opportunity_status import OpportunityStatus
        
        if not OpportunityStatus.is_valid_transition(current_status, new_status):
            raise ValidationException(
                f"Invalid status transition from {current_status.value} to {new_status.value}"
            )
        
        logger.info(f"Status transition from {current_status.value} to {new_status.value} validated successfully")
