"""
Service layer for the Opportunity Management Service.
"""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from .common import ValidationException, NotFoundException, OperationNotAllowedException, EventPublisher
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
from .enums import Priority, OpportunityStatus as StatusEnum, SkillType, ImportanceLevel, ProficiencyLevel
from .value_objects import GeographicRequirements
from .validators import (
    OpportunityValidator, ProblemStatementValidator, SkillRequirementValidator,
    TimelineValidator, AttachmentValidator, StatusTransitionValidator
)
from .repositories import (
    UserRepository, CustomerRepository, SkillsCatalogRepository,
    OpportunityRepository, ProblemStatementRepository, SkillRequirementRepository,
    TimelineRequirementRepository, OpportunityStatusRepository,
    AttachmentRepository, ChangeRecordRepository
)

logger = logging.getLogger(__name__)

class OpportunityService:
    """Service for managing opportunities."""
    
    def __init__(self, 
                opportunity_repository: OpportunityRepository,
                problem_statement_repository: ProblemStatementRepository,
                skill_requirement_repository: SkillRequirementRepository,
                timeline_requirement_repository: TimelineRequirementRepository,
                opportunity_status_repository: OpportunityStatusRepository,
                change_record_repository: ChangeRecordRepository,
                skills_catalog_repository: SkillsCatalogRepository,
                user_repository: UserRepository,
                customer_repository: CustomerRepository):
        """Initialize the service with repositories."""
        self.opportunity_repository = opportunity_repository
        self.problem_statement_repository = problem_statement_repository
        self.skill_requirement_repository = skill_requirement_repository
        self.timeline_requirement_repository = timeline_requirement_repository
        self.opportunity_status_repository = opportunity_status_repository
        self.change_record_repository = change_record_repository
        self.skills_catalog_repository = skills_catalog_repository
        self.user_repository = user_repository
        self.customer_repository = customer_repository
    
    def create_opportunity(self, title: str, customer_id: uuid.UUID, customer_name: str,
                         sales_manager_id: uuid.UUID, description: str, priority: Priority,
                         annual_recurring_revenue: float, geographic_requirements: Dict[str, Any]) -> Opportunity:
        """Create a new opportunity."""
        # Validate user is a sales manager
        user = self.user_repository.get_by_id(sales_manager_id)
        if not user or not user.is_sales_manager():
            raise OperationNotAllowedException("Only Sales Managers can create opportunities")
        
        # Validate customer exists
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise NotFoundException(f"Customer with ID {customer_id} not found")
        
        # Create geographic requirements value object
        geo_req = GeographicRequirements(
            region_id=uuid.UUID(geographic_requirements['region_id']),
            name=geographic_requirements['name'],
            requires_physical_presence=geographic_requirements['requires_physical_presence'],
            allows_remote_work=geographic_requirements['allows_remote_work']
        )
        
        # Validate required fields
        OpportunityValidator.validate_required_fields(
            title, description, customer_id, customer_name, sales_manager_id,
            priority, annual_recurring_revenue, geo_req
        )
        
        # Create opportunity
        opportunity = Opportunity.create_opportunity(
            title=title,
            customer_id=customer_id,
            customer_name=customer_name,
            sales_manager_id=sales_manager_id,
            description=description,
            priority=priority,
            annual_recurring_revenue=annual_recurring_revenue,
            geographic_requirements=geo_req
        )
        
        # Save opportunity
        saved_opportunity = self.opportunity_repository.add(opportunity)
        
        # Create initial status record
        status_record = OpportunityStatus.create_status_record(
            opportunity_id=saved_opportunity.id,
            status=StatusEnum.DRAFT,
            changed_by=sales_manager_id,
            reason="Opportunity created"
        )
        self.opportunity_status_repository.add(status_record)
        
        logger.info(f"Created opportunity with ID {saved_opportunity.id}")
        
        # Publish event
        EventPublisher.publish("opportunity.created", {"opportunity_id": str(saved_opportunity.id)})
        
        return saved_opportunity
    
    def add_problem_statement(self, opportunity_id: uuid.UUID, content: str) -> ProblemStatement:
        """Add a problem statement to an opportunity."""
        # Validate opportunity exists
        opportunity = self.opportunity_repository.get_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate opportunity is in Draft status
        if opportunity.status != StatusEnum.DRAFT:
            raise OperationNotAllowedException(
                "Problem statement can only be added to opportunities in Draft status"
            )
        
        # Validate content
        ProblemStatementValidator.validate_content(content)
        
        # Check if problem statement already exists
        existing_statement = self.problem_statement_repository.get_by_opportunity(opportunity_id)
        if existing_statement:
            raise OperationNotAllowedException(
                f"Problem statement already exists for opportunity {opportunity_id}"
            )
        
        # Create problem statement
        problem_statement = ProblemStatement.create_problem_statement(
            opportunity_id=opportunity_id,
            content=content
        )
        
        # Save problem statement
        saved_statement = self.problem_statement_repository.add(problem_statement)
        
        logger.info(f"Added problem statement to opportunity {opportunity_id}")
        
        return saved_statement
    
    def add_skill_requirement(self, opportunity_id: uuid.UUID, skill_id: uuid.UUID,
                            skill_type: SkillType, importance_level: ImportanceLevel,
                            minimum_proficiency_level: ProficiencyLevel) -> SkillRequirement:
        """Add a skill requirement to an opportunity."""
        # Validate opportunity exists
        opportunity = self.opportunity_repository.get_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate opportunity is in Draft status
        if opportunity.status != StatusEnum.DRAFT:
            raise OperationNotAllowedException(
                "Skill requirements can only be added to opportunities in Draft status"
            )
        
        # Validate skill exists in catalog
        skill = self.skills_catalog_repository.get_by_id(skill_id)
        if not skill:
            raise NotFoundException(f"Skill with ID {skill_id} not found in Skills Catalog")
        
        if not skill.is_active:
            raise ValidationException(f"Skill with ID {skill_id} is not active")
        
        # Create skill requirement
        skill_requirement = SkillRequirement.create_skill_requirement(
            opportunity_id=opportunity_id,
            skill_id=skill_id,
            skill_name=skill.name,
            skill_type=skill_type,
            importance_level=importance_level,
            minimum_proficiency_level=minimum_proficiency_level
        )
        
        # Save skill requirement
        saved_requirement = self.skill_requirement_repository.add(skill_requirement)
        
        logger.info(f"Added skill requirement for skill {skill.name} to opportunity {opportunity_id}")
        
        return saved_requirement
    
    def add_timeline_requirement(self, opportunity_id: uuid.UUID, start_date: str,
                               end_date: str, is_flexible: bool,
                               specific_days: Optional[List[str]] = None) -> TimelineRequirement:
        """Add a timeline requirement to an opportunity."""
        # Validate opportunity exists
        opportunity = self.opportunity_repository.get_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate opportunity is in Draft status
        if opportunity.status != StatusEnum.DRAFT:
            raise OperationNotAllowedException(
                "Timeline requirement can only be added to opportunities in Draft status"
            )
        
        # Validate timeline
        TimelineValidator.validate_timeline(start_date, end_date, specific_days)
        
        # Check if timeline requirement already exists
        existing_timeline = self.timeline_requirement_repository.get_by_opportunity(opportunity_id)
        if existing_timeline:
            raise OperationNotAllowedException(
                f"Timeline requirement already exists for opportunity {opportunity_id}"
            )
        
        # Create timeline requirement
        timeline_requirement = TimelineRequirement.create_timeline_requirement(
            opportunity_id=opportunity_id,
            start_date=start_date,
            end_date=end_date,
            is_flexible=is_flexible,
            specific_days=specific_days
        )
        
        # Save timeline requirement
        saved_timeline = self.timeline_requirement_repository.add(timeline_requirement)
        
        logger.info(f"Added timeline requirement to opportunity {opportunity_id}")
        
        return saved_timeline
    
    def submit_opportunity(self, opportunity_id: uuid.UUID, user_id: uuid.UUID) -> Opportunity:
        """Submit an opportunity for matching."""
        # Validate opportunity exists
        opportunity = self.opportunity_repository.get_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate user is authorized (owner or admin)
        if opportunity.sales_manager_id != user_id:
            user = self.user_repository.get_by_id(user_id)
            if not user or not user.is_admin():
                raise OperationNotAllowedException(
                    "Only the Sales Manager who created the opportunity or an Admin can submit it"
                )
        
        # Validate problem statement exists and meets requirements
        problem_statement = self.problem_statement_repository.get_by_opportunity(opportunity_id)
        if not problem_statement:
            raise ValidationException("Problem statement is required before submission")
        
        # Validate problem statement meets minimum length
        ProblemStatementValidator.validate_content(problem_statement.content)
        
        # Validate at least one skill requirement exists
        skill_requirements = self.skill_requirement_repository.get_by_opportunity(opportunity_id)
        if not skill_requirements:
            raise ValidationException("At least one skill requirement is required before submission")
        
        # Validate at least one "Must Have" skill
        SkillRequirementValidator.validate_skill_requirements(skill_requirements)
        
        # Validate timeline requirement exists
        timeline = self.timeline_requirement_repository.get_by_opportunity(opportunity_id)
        if not timeline:
            raise ValidationException("Timeline requirement is required before submission")
        
        # Update opportunity status
        opportunity.status = StatusEnum.SUBMITTED
        opportunity.submitted_at = datetime.now()
        opportunity.update()
        
        # Save updated opportunity
        updated_opportunity = self.opportunity_repository.update(opportunity)
        
        # Create status record
        status_record = OpportunityStatus.create_status_record(
            opportunity_id=opportunity_id,
            status=StatusEnum.SUBMITTED,
            changed_by=user_id,
            reason="Opportunity submitted for matching"
        )
        self.opportunity_status_repository.add(status_record)
        
        # Create change record
        change_record = ChangeRecord.create_change_record(
            opportunity_id=opportunity_id,
            changed_by=user_id,
            field_changed="status",
            reason="Opportunity submitted for matching",
            old_value=StatusEnum.DRAFT.value,
            new_value=StatusEnum.SUBMITTED.value
        )
        self.change_record_repository.add(change_record)
        
        logger.info(f"Submitted opportunity {opportunity_id} for matching")
        
        # Publish event
        EventPublisher.publish("opportunity.submitted", {"opportunity_id": str(opportunity_id)})
        
        return updated_opportunity
    
    def cancel_opportunity(self, opportunity_id: uuid.UUID, user_id: uuid.UUID, reason: str) -> Opportunity:
        """Cancel an opportunity."""
        # Validate opportunity exists
        opportunity = self.opportunity_repository.get_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate user is authorized (owner or admin)
        if opportunity.sales_manager_id != user_id:
            user = self.user_repository.get_by_id(user_id)
            if not user or not user.is_admin():
                raise OperationNotAllowedException(
                    "Only the Sales Manager who created the opportunity or an Admin can cancel it"
                )
        
        # Validate opportunity is not already completed
        if opportunity.status == StatusEnum.COMPLETED:
            raise OperationNotAllowedException("Completed opportunities cannot be cancelled")
        
        # Validate reason is provided
        if not reason:
            raise ValidationException("Cancellation reason is required")
        
        # Store previous status for change record
        previous_status = opportunity.status
        
        # Update opportunity
        opportunity.status = StatusEnum.CANCELLED
        opportunity.cancelled_at = datetime.now()
        opportunity.cancellation_reason = reason
        opportunity.reactivation_deadline = datetime.now() + timedelta(days=90)
        opportunity.update()
        
        # Save updated opportunity
        updated_opportunity = self.opportunity_repository.update(opportunity)
        
        # Create status record
        status_record = OpportunityStatus.create_status_record(
            opportunity_id=opportunity_id,
            status=StatusEnum.CANCELLED,
            changed_by=user_id,
            reason=reason
        )
        self.opportunity_status_repository.add(status_record)
        
        # Create change record
        change_record = ChangeRecord.create_change_record(
            opportunity_id=opportunity_id,
            changed_by=user_id,
            field_changed="status",
            reason=reason,
            old_value=previous_status.value,
            new_value=StatusEnum.CANCELLED.value
        )
        self.change_record_repository.add(change_record)
        
        logger.info(f"Cancelled opportunity {opportunity_id}")
        
        # Publish event
        EventPublisher.publish("opportunity.cancelled", {
            "opportunity_id": str(opportunity_id),
            "reason": reason
        })
        
        return updated_opportunity
    
    def reactivate_opportunity(self, opportunity_id: uuid.UUID, user_id: uuid.UUID) -> Opportunity:
        """Reactivate a cancelled opportunity."""
        # Validate opportunity exists
        opportunity = self.opportunity_repository.get_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate user is authorized (owner or admin)
        if opportunity.sales_manager_id != user_id:
            user = self.user_repository.get_by_id(user_id)
            if not user or not user.is_admin():
                raise OperationNotAllowedException(
                    "Only the Sales Manager who created the opportunity or an Admin can reactivate it"
                )
        
        # Validate opportunity is cancelled
        if opportunity.status != StatusEnum.CANCELLED:
            raise OperationNotAllowedException("Only cancelled opportunities can be reactivated")
        
        # Validate reactivation deadline
        if not opportunity.reactivation_deadline or datetime.now() > opportunity.reactivation_deadline:
            raise OperationNotAllowedException(
                "Opportunity cannot be reactivated after the reactivation deadline (90 days)"
            )
        
        # Get status history to determine previous status
        status_history = self.opportunity_status_repository.get_status_history(opportunity_id)
        
        # Find the status before cancellation
        previous_status = StatusEnum.DRAFT  # Default if we can't determine
        for i in range(len(status_history) - 2, -1, -1):
            if status_history[i].status != StatusEnum.CANCELLED:
                previous_status = status_history[i].status
                break
        
        # Update opportunity
        opportunity.status = previous_status
        opportunity.cancelled_at = None
        opportunity.cancellation_reason = None
        opportunity.reactivation_deadline = None
        opportunity.update()
        
        # Save updated opportunity
        updated_opportunity = self.opportunity_repository.update(opportunity)
        
        # Create status record
        status_record = OpportunityStatus.create_status_record(
            opportunity_id=opportunity_id,
            status=previous_status,
            changed_by=user_id,
            reason="Opportunity reactivated"
        )
        self.opportunity_status_repository.add(status_record)
        
        # Create change record
        change_record = ChangeRecord.create_change_record(
            opportunity_id=opportunity_id,
            changed_by=user_id,
            field_changed="status",
            reason="Opportunity reactivated",
            old_value=StatusEnum.CANCELLED.value,
            new_value=previous_status.value
        )
        self.change_record_repository.add(change_record)
        
        logger.info(f"Reactivated opportunity {opportunity_id}")
        
        # Publish event
        EventPublisher.publish("opportunity.reactivated", {"opportunity_id": str(opportunity_id)})
        
        return updated_opportunity
    
    def get_opportunity_details(self, opportunity_id: uuid.UUID) -> Dict[str, Any]:
        """Get comprehensive details about an opportunity."""
        # Validate opportunity exists
        opportunity = self.opportunity_repository.get_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Get related entities
        problem_statement = self.problem_statement_repository.get_by_opportunity(opportunity_id)
        skill_requirements = self.skill_requirement_repository.get_by_opportunity(opportunity_id)
        timeline = self.timeline_requirement_repository.get_by_opportunity(opportunity_id)
        status_history = self.opportunity_status_repository.get_status_history(opportunity_id)
        change_history = self.change_record_repository.get_by_opportunity(opportunity_id)
        
        # Get attachments if problem statement exists
        attachments = []
        if problem_statement:
            attachments = self.attachment_service.get_attachments_for_problem_statement(problem_statement.id)
        
        # Compile details
        details = {
            "opportunity": opportunity,
            "problem_statement": problem_statement,
            "skill_requirements": skill_requirements,
            "timeline": timeline,
            "status_history": status_history,
            "change_history": change_history,
            "attachments": attachments
        }
        
        return details
    
    def search_opportunities(self, query: str = None, status: str = None, 
                           priority: str = None, sales_manager_id: uuid.UUID = None,
                           customer_id: uuid.UUID = None) -> List[Opportunity]:
        """Search for opportunities with various filters."""
        # Start with all opportunities
        opportunities = self.opportunity_repository.get_all()
        
        # Apply filters
        if query:
            opportunities = [opp for opp in opportunities 
                            if query.lower() in opp.title.lower() or 
                            query.lower() in opp.description.lower()]
        
        if status:
            opportunities = [opp for opp in opportunities if opp.status.value == status]
        
        if priority:
            opportunities = [opp for opp in opportunities if opp.priority.value == priority]
        
        if sales_manager_id:
            opportunities = [opp for opp in opportunities if opp.sales_manager_id == sales_manager_id]
        
        if customer_id:
            opportunities = [opp for opp in opportunities if opp.customer_id == customer_id]
        
        return opportunities

class AttachmentService:
    """Service for managing attachments."""
    
    def __init__(self, attachment_repository: AttachmentRepository,
                problem_statement_repository: ProblemStatementRepository):
        """Initialize the service with repositories."""
        self.attachment_repository = attachment_repository
        self.problem_statement_repository = problem_statement_repository
    
    def add_attachment(self, problem_statement_id: uuid.UUID, file_name: str,
                     file_type: str, file_size: int, file_url: str,
                     uploaded_by: uuid.UUID) -> Attachment:
        """Add an attachment to a problem statement."""
        # Validate problem statement exists
        problem_statement = self.problem_statement_repository.get_by_id(problem_statement_id)
        if not problem_statement:
            raise NotFoundException(f"Problem statement with ID {problem_statement_id} not found")
        
        # Validate attachment
        AttachmentValidator.validate_attachment(file_name, file_type, file_size)
        
        # Create attachment
        attachment = Attachment.create_attachment(
            problem_statement_id=problem_statement_id,
            file_name=file_name,
            file_type=file_type,
            file_size=file_size,
            file_url=file_url,
            uploaded_by=uploaded_by
        )
        
        # Save attachment
        saved_attachment = self.attachment_repository.add(attachment)
        
        logger.info(f"Added attachment {file_name} to problem statement {problem_statement_id}")
        
        return saved_attachment
    
    def remove_attachment(self, attachment_id: uuid.UUID, user_id: uuid.UUID) -> Attachment:
        """Remove an attachment."""
        # Validate attachment exists
        attachment = self.attachment_repository.get_by_id(attachment_id)
        if not attachment:
            raise NotFoundException(f"Attachment with ID {attachment_id} not found")
        
        # Mark attachment as removed
        attachment.remove_attachment()
        
        # Save updated attachment
        updated_attachment = self.attachment_repository.update(attachment)
        
        logger.info(f"Removed attachment {attachment_id}")
        
        return updated_attachment
    
    def get_attachments_for_problem_statement(self, problem_statement_id: uuid.UUID) -> List[Attachment]:
        """Get all attachments for a problem statement."""
        return self.attachment_repository.get_active_attachments(problem_statement_id)
