"""
Service adapter to bridge API layer with domain services.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.models.opportunity import Opportunity
from app.models.problem_statement import ProblemStatement
from app.models.skill_requirement import SkillRequirement
from app.models.timeline_requirement import TimelineRequirement
from app.models.opportunity_status import OpportunityStatus
from app.models.change_record import ChangeRecord
from app.core.exceptions import ValidationException, NotFoundException, OperationNotAllowedException


class OpportunityServiceAdapter:
    """Adapter service for opportunity operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_opportunity(
        self,
        title: str,
        customer_id: uuid.UUID,
        customer_name: str,
        sales_manager_id: uuid.UUID,
        description: str,
        priority: str,
        annual_recurring_revenue: float,
        geographic_requirements: Dict[str, Any]
    ) -> Opportunity:
        """Create a new opportunity."""
        # Basic validation
        if not title or len(title.strip()) == 0:
            raise ValidationException("Title is required")
        
        if annual_recurring_revenue < 0:
            raise ValidationException("Annual recurring revenue must be non-negative")
        
        # Convert UUID objects to strings in geographic_requirements
        geo_reqs = geographic_requirements.copy()
        if 'region_id' in geo_reqs and hasattr(geo_reqs['region_id'], '__str__'):
            geo_reqs['region_id'] = str(geo_reqs['region_id'])
        
        # Create opportunity
        opportunity = Opportunity(
            title=title,
            customer_id=str(customer_id),
            customer_name=customer_name,
            sales_manager_id=str(sales_manager_id),
            description=description,
            priority=priority,
            annual_recurring_revenue=annual_recurring_revenue,
            geographic_requirements=geo_reqs,
            status="DRAFT"
        )
        
        self.db.add(opportunity)
        self.db.commit()
        self.db.refresh(opportunity)
        
        # Create initial status record
        status_record = OpportunityStatus(
            opportunity_id=opportunity.id,
            status="DRAFT",
            changed_by=str(sales_manager_id),
            reason="Opportunity created"
        )
        self.db.add(status_record)
        self.db.commit()
        
        return opportunity
    
    def get_opportunity_by_id(self, opportunity_id: uuid.UUID) -> Optional[Opportunity]:
        """Get opportunity by ID."""
        return self.db.query(Opportunity).filter(Opportunity.id == str(opportunity_id)).first()
    
    def add_problem_statement(self, opportunity_id: uuid.UUID, content: str) -> ProblemStatement:
        """Add a problem statement to an opportunity."""
        # Validate opportunity exists
        opportunity = self.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate opportunity is in Draft status
        if opportunity.status != "DRAFT":
            raise OperationNotAllowedException(
                "Problem statement can only be added to opportunities in Draft status"
            )
        
        # Validate content length
        if len(content.strip()) < 100:
            raise ValidationException("Problem statement must be at least 100 characters long")
        
        # Check if problem statement already exists
        existing_statement = self.db.query(ProblemStatement).filter(
            ProblemStatement.opportunity_id == str(opportunity_id)
        ).first()
        if existing_statement:
            raise OperationNotAllowedException(
                f"Problem statement already exists for opportunity {opportunity_id}"
            )
        
        # Create problem statement
        problem_statement = ProblemStatement(
            opportunity_id=str(opportunity_id),
            content=content
        )
        
        self.db.add(problem_statement)
        self.db.commit()
        self.db.refresh(problem_statement)
        
        return problem_statement
    
    def add_skill_requirement(
        self,
        opportunity_id: uuid.UUID,
        skill_id: uuid.UUID,
        skill_name: str,
        skill_type: str,
        importance_level: str,
        minimum_proficiency_level: str
    ) -> SkillRequirement:
        """Add a skill requirement to an opportunity."""
        # Validate opportunity exists
        opportunity = self.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate opportunity is in Draft status
        if opportunity.status != "DRAFT":
            raise OperationNotAllowedException(
                "Skill requirements can only be added to opportunities in Draft status"
            )
        
        # Create skill requirement with the provided skill_name
        skill_requirement = SkillRequirement(
            opportunity_id=str(opportunity_id),
            skill_id=str(skill_id),
            skill_name=skill_name,
            skill_type=skill_type,
            importance_level=importance_level,
            minimum_proficiency_level=minimum_proficiency_level
        )
        
        self.db.add(skill_requirement)
        self.db.commit()
        self.db.refresh(skill_requirement)
        
        return skill_requirement
    
    def add_timeline_requirement(
        self,
        opportunity_id: uuid.UUID,
        start_date: str,
        end_date: str,
        is_flexible: bool,
        specific_days: Optional[List[str]] = None
    ) -> TimelineRequirement:
        """Add a timeline requirement to an opportunity."""
        # Validate opportunity exists
        opportunity = self.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate opportunity is in Draft status
        if opportunity.status != "DRAFT":
            raise OperationNotAllowedException(
                "Timeline requirement can only be added to opportunities in Draft status"
            )
        
        # Check if timeline requirement already exists
        existing_timeline = self.db.query(TimelineRequirement).filter(
            TimelineRequirement.opportunity_id == str(opportunity_id)
        ).first()
        if existing_timeline:
            raise OperationNotAllowedException(
                f"Timeline requirement already exists for opportunity {opportunity_id}"
            )
        
        # Create timeline requirement
        timeline_requirement = TimelineRequirement(
            opportunity_id=str(opportunity_id),
            start_date=start_date,
            end_date=end_date,
            is_flexible=is_flexible,
            specific_days=specific_days
        )
        
        self.db.add(timeline_requirement)
        self.db.commit()
        self.db.refresh(timeline_requirement)
        
        return timeline_requirement
    
    def submit_opportunity(self, opportunity_id: uuid.UUID, user_id: uuid.UUID) -> Opportunity:
        """Submit an opportunity for matching."""
        # Validate opportunity exists
        opportunity = self.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate opportunity is in Draft status
        if opportunity.status != "DRAFT":
            raise OperationNotAllowedException("Only draft opportunities can be submitted")
        
        # Validate problem statement exists
        problem_statement = self.db.query(ProblemStatement).filter(
            ProblemStatement.opportunity_id == str(opportunity_id)
        ).first()
        if not problem_statement:
            raise ValidationException("Problem statement is required before submission")
        
        # Validate at least one skill requirement exists
        skill_requirements = self.db.query(SkillRequirement).filter(
            SkillRequirement.opportunity_id == str(opportunity_id)
        ).all()
        if not skill_requirements:
            raise ValidationException("At least one skill requirement is required before submission")
        
        # Validate at least one "MUST_HAVE" skill
        must_have_skills = [sr for sr in skill_requirements if sr.importance_level == "MUST_HAVE"]
        if not must_have_skills:
            raise ValidationException("At least one 'Must Have' skill requirement is required")
        
        # Validate timeline requirement exists
        timeline = self.db.query(TimelineRequirement).filter(
            TimelineRequirement.opportunity_id == str(opportunity_id)
        ).first()
        if not timeline:
            raise ValidationException("Timeline requirement is required before submission")
        
        # Update opportunity status
        opportunity.status = "SUBMITTED"
        opportunity.submitted_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(opportunity)
        
        # Create status record
        status_record = OpportunityStatus(
            opportunity_id=opportunity.id,
            status="SUBMITTED",
            changed_by=str(user_id),
            reason="Opportunity submitted for matching"
        )
        self.db.add(status_record)
        
        # Create change record
        change_record = ChangeRecord(
            opportunity_id=opportunity.id,
            changed_by=str(user_id),
            field_changed="status",
            reason="Opportunity submitted for matching",
            old_value="DRAFT",
            new_value="SUBMITTED"
        )
        self.db.add(change_record)
        
        self.db.commit()
        
        return opportunity
    
    def cancel_opportunity(self, opportunity_id: uuid.UUID, user_id: uuid.UUID, reason: str) -> Opportunity:
        """Cancel an opportunity."""
        # Validate opportunity exists
        opportunity = self.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate opportunity is not already completed
        if opportunity.status == "COMPLETED":
            raise OperationNotAllowedException("Completed opportunities cannot be cancelled")
        
        # Validate reason is provided
        if not reason or len(reason.strip()) == 0:
            raise ValidationException("Cancellation reason is required")
        
        # Store previous status for change record
        previous_status = opportunity.status
        
        # Update opportunity
        opportunity.status = "CANCELLED"
        opportunity.cancelled_at = datetime.utcnow()
        opportunity.cancellation_reason = reason
        opportunity.reactivation_deadline = datetime.utcnow()  # Simplified - should be +90 days
        
        self.db.commit()
        self.db.refresh(opportunity)
        
        # Create status record
        status_record = OpportunityStatus(
            opportunity_id=opportunity.id,
            status="CANCELLED",
            changed_by=str(user_id),
            reason=reason
        )
        self.db.add(status_record)
        
        # Create change record
        change_record = ChangeRecord(
            opportunity_id=opportunity.id,
            changed_by=str(user_id),
            field_changed="status",
            reason=reason,
            old_value=previous_status,
            new_value="CANCELLED"
        )
        self.db.add(change_record)
        
        self.db.commit()
        
        return opportunity
    
    def reactivate_opportunity(self, opportunity_id: uuid.UUID, user_id: uuid.UUID) -> Opportunity:
        """Reactivate a cancelled opportunity."""
        # Validate opportunity exists
        opportunity = self.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate opportunity is cancelled
        if opportunity.status != "CANCELLED":
            raise OperationNotAllowedException("Only cancelled opportunities can be reactivated")
        
        # Get status history to determine previous status
        status_history = self.db.query(OpportunityStatus).filter(
            OpportunityStatus.opportunity_id == opportunity.id
        ).order_by(OpportunityStatus.changed_at.desc()).all()
        
        # Find the status before cancellation
        previous_status = "DRAFT"  # Default
        for status_record in status_history[1:]:  # Skip the current CANCELLED status
            if status_record.status != "CANCELLED":
                previous_status = status_record.status
                break
        
        # Update opportunity
        opportunity.status = previous_status
        opportunity.cancelled_at = None
        opportunity.cancellation_reason = None
        opportunity.reactivation_deadline = None
        
        self.db.commit()
        self.db.refresh(opportunity)
        
        # Create status record
        status_record = OpportunityStatus(
            opportunity_id=opportunity.id,
            status=previous_status,
            changed_by=str(user_id),
            reason="Opportunity reactivated"
        )
        self.db.add(status_record)
        
        # Create change record
        change_record = ChangeRecord(
            opportunity_id=opportunity.id,
            changed_by=str(user_id),
            field_changed="status",
            reason="Opportunity reactivated",
            old_value="CANCELLED",
            new_value=previous_status
        )
        self.db.add(change_record)
        
        self.db.commit()
        
        return opportunity
    
    def get_opportunity_details(self, opportunity_id: uuid.UUID) -> Dict[str, Any]:
        """Get comprehensive details about an opportunity."""
        # Validate opportunity exists
        opportunity = self.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise NotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Get related entities
        problem_statement = self.db.query(ProblemStatement).filter(
            ProblemStatement.opportunity_id == str(opportunity_id)
        ).first()
        
        skill_requirements = self.db.query(SkillRequirement).filter(
            SkillRequirement.opportunity_id == str(opportunity_id)
        ).all()
        
        timeline = self.db.query(TimelineRequirement).filter(
            TimelineRequirement.opportunity_id == str(opportunity_id)
        ).first()
        
        status_history = self.db.query(OpportunityStatus).filter(
            OpportunityStatus.opportunity_id == opportunity.id
        ).order_by(OpportunityStatus.changed_at.desc()).all()
        
        change_history = self.db.query(ChangeRecord).filter(
            ChangeRecord.opportunity_id == opportunity.id
        ).order_by(ChangeRecord.changed_at.desc()).all()
        
        # Get attachments if problem statement exists
        attachments = []
        if problem_statement:
            from app.models.attachment import Attachment
            attachments = self.db.query(Attachment).filter(
                Attachment.problem_statement_id == problem_statement.id,
                Attachment.is_removed == False
            ).all()
        
        return {
            "opportunity": opportunity,
            "problem_statement": problem_statement,
            "skill_requirements": skill_requirements,
            "timeline": timeline,
            "status_history": status_history,
            "change_history": change_history,
            "attachments": attachments
        }
    
    def search_opportunities(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        sales_manager_id: Optional[uuid.UUID] = None,
        customer_id: Optional[uuid.UUID] = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[Opportunity], int]:
        """Search for opportunities with various filters."""
        # Start with base query
        query_obj = self.db.query(Opportunity)
        
        # Apply filters
        if query:
            query_obj = query_obj.filter(
                (Opportunity.title.ilike(f"%{query}%")) |
                (Opportunity.description.ilike(f"%{query}%"))
            )
        
        if status:
            query_obj = query_obj.filter(Opportunity.status == status)
        
        if priority:
            query_obj = query_obj.filter(Opportunity.priority == priority)
        
        if sales_manager_id:
            query_obj = query_obj.filter(Opportunity.sales_manager_id == str(sales_manager_id))
        
        if customer_id:
            query_obj = query_obj.filter(Opportunity.customer_id == str(customer_id))
        
        # Get total count
        total_count = query_obj.count()
        
        # Apply pagination
        offset = (page - 1) * page_size
        opportunities = query_obj.offset(offset).limit(page_size).all()
        
        return opportunities, total_count
