"""
Opportunity entity - the main aggregate root for opportunity management.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Dict, Any, List, Optional
from decimal import Decimal

from .aggregate_root import AggregateRoot
from ..enums.status import OpportunityStatus
from ..enums.priority import Priority
from ..value_objects.skill_requirement import SkillRequirement
from ..value_objects.timeline_specification import TimelineSpecification
from ..value_objects.geographic_requirement import GeographicRequirement
from ..value_objects.language_requirement import LanguageRequirements
from .problem_statement import ProblemStatement
from .status_history import StatusHistory


@dataclass
class Opportunity(AggregateRoot):
    """Main aggregate root representing a customer opportunity."""
    
    # Core identification
    title: str = ""
    description: str = ""
    customer_id: str = ""
    sales_manager_id: str = ""
    
    # Business attributes
    annual_recurring_revenue: Decimal = field(default_factory=lambda: Decimal("0"))
    priority: Priority = Priority.MEDIUM
    status: OpportunityStatus = OpportunityStatus.DRAFT
    
    # Requirements
    problem_statement: Optional[ProblemStatement] = None
    skill_requirements: List[SkillRequirement] = field(default_factory=list)
    timeline_specification: Optional[TimelineSpecification] = None
    geographic_requirement: Optional[GeographicRequirement] = None
    language_requirements: Optional[LanguageRequirements] = None
    
    # Status tracking
    status_history: List[StatusHistory] = field(default_factory=list)
    
    # Metadata
    selected_architect_id: Optional[str] = None
    completion_date: Optional[date] = None
    cancellation_date: Optional[date] = None
    cancellation_reason: Optional[str] = None
    
    def __post_init__(self):
        """Validate opportunity after initialization."""
        super().__post_init__()
        
        if not self.title or not self.title.strip():
            raise ValueError("Opportunity title cannot be empty")
        
        if not self.description or not self.description.strip():
            raise ValueError("Opportunity description cannot be empty")
        
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("Customer ID cannot be empty")
        
        if not self.sales_manager_id or not self.sales_manager_id.strip():
            raise ValueError("Sales Manager ID cannot be empty")
        
        if self.annual_recurring_revenue <= 0:
            raise ValueError("Annual Recurring Revenue must be positive")
        
        # Create initial status history if none exists
        if not self.status_history:
            initial_history = StatusHistory.create_initial_status(
                opportunity_id=self.id,
                initial_status=self.status,
                created_by=self.sales_manager_id,
                notes="Opportunity created"
            )
            self.status_history.append(initial_history)
    
    def update_basic_info(self, title: Optional[str] = None, 
                         description: Optional[str] = None,
                         annual_recurring_revenue: Optional[Decimal] = None,
                         priority: Optional[Priority] = None) -> None:
        """Update basic opportunity information."""
        if not self.status.is_modifiable:
            raise ValueError(f"Cannot modify opportunity in {self.status} status")
        
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            self.title = title
        
        if description is not None:
            if not description.strip():
                raise ValueError("Description cannot be empty")
            self.description = description
        
        if annual_recurring_revenue is not None:
            if annual_recurring_revenue <= 0:
                raise ValueError("Annual Recurring Revenue must be positive")
            self.annual_recurring_revenue = annual_recurring_revenue
        
        if priority is not None:
            self.priority = priority
        
        self.update_timestamp()
    
    def set_problem_statement(self, problem_statement: ProblemStatement) -> None:
        """Set the problem statement for the opportunity."""
        if not self.status.is_modifiable:
            raise ValueError(f"Cannot modify opportunity in {self.status} status")
        
        self.problem_statement = problem_statement
        self.update_timestamp()
    
    def add_skill_requirement(self, skill_requirement: SkillRequirement) -> None:
        """Add a skill requirement to the opportunity."""
        if not self.status.is_modifiable:
            raise ValueError(f"Cannot modify opportunity in {self.status} status")
        
        # Check for duplicate skills
        for existing_skill in self.skill_requirements:
            if (existing_skill.skill_name.lower() == skill_requirement.skill_name.lower() and
                existing_skill.skill_category == skill_requirement.skill_category):
                raise ValueError(f"Skill requirement already exists: {skill_requirement.skill_name}")
        
        self.skill_requirements.append(skill_requirement)
        self.update_timestamp()
    
    def remove_skill_requirement(self, skill_name: str, skill_category: str) -> bool:
        """Remove a skill requirement from the opportunity."""
        if not self.status.is_modifiable:
            raise ValueError(f"Cannot modify opportunity in {self.status} status")
        
        for i, skill in enumerate(self.skill_requirements):
            if (skill.skill_name.lower() == skill_name.lower() and 
                skill.skill_category == skill_category):
                del self.skill_requirements[i]
                self.update_timestamp()
                return True
        return False
    
    def set_timeline_specification(self, timeline_spec: TimelineSpecification) -> None:
        """Set the timeline specification for the opportunity."""
        if not self.status.is_modifiable:
            raise ValueError(f"Cannot modify opportunity in {self.status} status")
        
        self.timeline_specification = timeline_spec
        self.update_timestamp()
    
    def set_geographic_requirement(self, geo_requirement: GeographicRequirement) -> None:
        """Set the geographic requirement for the opportunity."""
        if not self.status.is_modifiable:
            raise ValueError(f"Cannot modify opportunity in {self.status} status")
        
        self.geographic_requirement = geo_requirement
        self.update_timestamp()
    
    def set_language_requirements(self, lang_requirements: LanguageRequirements) -> None:
        """Set the language requirements for the opportunity."""
        if not self.status.is_modifiable:
            raise ValueError(f"Cannot modify opportunity in {self.status} status")
        
        self.language_requirements = lang_requirements
        self.update_timestamp()
    
    def change_status(self, new_status: OpportunityStatus, changed_by: str, 
                     reason: Optional[str] = None, notes: Optional[str] = None) -> None:
        """Change the opportunity status with validation."""
        if not self.status.can_transition_to(new_status):
            raise ValueError(f"Cannot transition from {self.status} to {new_status}")
        
        # Create status history entry
        status_change = StatusHistory.create_status_change(
            opportunity_id=self.id,
            from_status=self.status,
            to_status=new_status,
            changed_by=changed_by,
            reason=reason,
            notes=notes
        )
        
        self.status_history.append(status_change)
        self.status = new_status
        
        # Handle special status changes
        if new_status == OpportunityStatus.CANCELLED:
            self.cancellation_date = date.today()
            self.cancellation_reason = reason
        elif new_status == OpportunityStatus.COMPLETED:
            self.completion_date = date.today()
        
        self.update_timestamp()
    
    def select_architect(self, architect_id: str, selected_by: str) -> None:
        """Select a solution architect for the opportunity."""
        if self.status != OpportunityStatus.MATCHES_FOUND:
            raise ValueError("Can only select architect when matches are found")
        
        self.selected_architect_id = architect_id
        self.change_status(OpportunityStatus.ARCHITECT_SELECTED, selected_by, 
                          "Solution Architect selected")
    
    def complete_opportunity(self, completed_by: str, notes: Optional[str] = None) -> None:
        """Mark the opportunity as completed."""
        if self.status != OpportunityStatus.ARCHITECT_SELECTED:
            raise ValueError("Can only complete opportunity after architect is selected")
        
        self.change_status(OpportunityStatus.COMPLETED, completed_by, 
                          "Opportunity completed", notes)
    
    def cancel_opportunity(self, cancelled_by: str, reason: str, notes: Optional[str] = None) -> None:
        """Cancel the opportunity."""
        if self.status.is_final:
            raise ValueError("Cannot cancel a completed or already cancelled opportunity")
        
        if not reason or not reason.strip():
            raise ValueError("Cancellation reason is required")
        
        self.change_status(OpportunityStatus.CANCELLED, cancelled_by, reason, notes)
    
    def reactivate_opportunity(self, reactivated_by: str, notes: Optional[str] = None) -> None:
        """Reactivate a cancelled opportunity within the allowed timeframe."""
        if self.status != OpportunityStatus.CANCELLED:
            raise ValueError("Can only reactivate cancelled opportunities")
        
        if not self.cancellation_date:
            raise ValueError("Cancellation date not found")
        
        # Check 90-day reactivation window
        days_since_cancellation = (date.today() - self.cancellation_date).days
        if days_since_cancellation > 90:
            raise ValueError("Cannot reactivate opportunity after 90 days")
        
        self.change_status(OpportunityStatus.DRAFT, reactivated_by, 
                          "Opportunity reactivated", notes)
        self.cancellation_date = None
        self.cancellation_reason = None
    
    def clone_opportunity(self, new_title: str, cloned_by: str) -> 'Opportunity':
        """Create a clone of this opportunity with a new title."""
        cloned = Opportunity(
            title=new_title,
            description=self.description,
            customer_id=self.customer_id,
            sales_manager_id=cloned_by,
            annual_recurring_revenue=self.annual_recurring_revenue,
            priority=self.priority,
            skill_requirements=self.skill_requirements.copy(),
            timeline_specification=self.timeline_specification,
            geographic_requirement=self.geographic_requirement,
            language_requirements=self.language_requirements
        )
        
        # Clone problem statement if exists
        if self.problem_statement:
            cloned.problem_statement = ProblemStatement(
                title=self.problem_statement.title,
                description=self.problem_statement.description,
                business_impact=self.problem_statement.business_impact,
                technical_requirements=self.problem_statement.technical_requirements,
                success_criteria=self.problem_statement.success_criteria,
                constraints=self.problem_statement.constraints
                # Note: Attachments are not cloned for security reasons
            )
        
        return cloned
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert opportunity to dictionary representation."""
        base_dict = super().to_dict()
        base_dict.update({
            "title": self.title,
            "description": self.description,
            "customer_id": self.customer_id,
            "sales_manager_id": self.sales_manager_id,
            "annual_recurring_revenue": str(self.annual_recurring_revenue),
            "priority": self.priority.value,
            "status": self.status.value,
            "problem_statement": self.problem_statement.to_dict() if self.problem_statement else None,
            "skill_requirements": [skill.to_dict() for skill in self.skill_requirements],
            "timeline_specification": self.timeline_specification.to_dict() if self.timeline_specification else None,
            "geographic_requirement": self.geographic_requirement.to_dict() if self.geographic_requirement else None,
            "language_requirements": self.language_requirements.to_dict() if self.language_requirements else None,
            "status_history": [history.to_dict() for history in self.status_history],
            "selected_architect_id": self.selected_architect_id,
            "completion_date": self.completion_date.isoformat() if self.completion_date else None,
            "cancellation_date": self.cancellation_date.isoformat() if self.cancellation_date else None,
            "cancellation_reason": self.cancellation_reason
        })
        return base_dict
    
    @property
    def is_ready_for_matching(self) -> bool:
        """Check if opportunity is ready for matching process."""
        return (self.status == OpportunityStatus.SUBMITTED and
                self.problem_statement is not None and
                len(self.skill_requirements) > 0 and
                self.timeline_specification is not None)
    
    @property
    def mandatory_skills(self) -> List[SkillRequirement]:
        """Get all mandatory skill requirements."""
        return [skill for skill in self.skill_requirements if skill.is_mandatory]
    
    @property
    def optional_skills(self) -> List[SkillRequirement]:
        """Get all optional skill requirements."""
        return [skill for skill in self.skill_requirements if not skill.is_mandatory]
    
    def __str__(self) -> str:
        """String representation of opportunity."""
        return f"Opportunity(id={self.id}, title={self.title}, status={self.status})"
