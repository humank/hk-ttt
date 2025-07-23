"""
Sample usage examples for the Opportunity Management Service.
"""

import uuid
import logging
from datetime import datetime, timedelta

from .enums import Priority, OpportunityStatus, SkillType, ImportanceLevel, ProficiencyLevel, UserRole
from .value_objects import GeographicRequirements
from .user import User
from .customer import Customer
from .skills_catalog import SkillsCatalog
from .in_memory_repositories import (
    InMemoryUserRepository, InMemoryCustomerRepository, InMemorySkillsCatalogRepository,
    InMemoryOpportunityRepository, InMemoryProblemStatementRepository, InMemorySkillRequirementRepository,
    InMemoryTimelineRequirementRepository, InMemoryOpportunityStatusRepository,
    InMemoryAttachmentRepository, InMemoryChangeRecordRepository
)
from .services import OpportunityService, AttachmentService
from .common import EventPublisher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_repositories_and_services():
    """Set up repositories and services."""
    # Create repositories
    user_repository = InMemoryUserRepository()
    customer_repository = InMemoryCustomerRepository()
    skills_catalog_repository = InMemorySkillsCatalogRepository()
    opportunity_repository = InMemoryOpportunityRepository()
    problem_statement_repository = InMemoryProblemStatementRepository()
    skill_requirement_repository = InMemorySkillRequirementRepository()
    timeline_requirement_repository = InMemoryTimelineRequirementRepository()
    opportunity_status_repository = InMemoryOpportunityStatusRepository()
    attachment_repository = InMemoryAttachmentRepository()
    change_record_repository = InMemoryChangeRecordRepository()
    
    # Create services
    attachment_service = AttachmentService(
        attachment_repository=attachment_repository,
        problem_statement_repository=problem_statement_repository
    )
    
    opportunity_service = OpportunityService(
        opportunity_repository=opportunity_repository,
        problem_statement_repository=problem_statement_repository,
        skill_requirement_repository=skill_requirement_repository,
        timeline_requirement_repository=timeline_requirement_repository,
        opportunity_status_repository=opportunity_status_repository,
        change_record_repository=change_record_repository,
        skills_catalog_repository=skills_catalog_repository,
        user_repository=user_repository,
        customer_repository=customer_repository
    )
    
    return {
        "repositories": {
            "user": user_repository,
            "customer": customer_repository,
            "skills_catalog": skills_catalog_repository,
            "opportunity": opportunity_repository,
            "problem_statement": problem_statement_repository,
            "skill_requirement": skill_requirement_repository,
            "timeline_requirement": timeline_requirement_repository,
            "opportunity_status": opportunity_status_repository,
            "attachment": attachment_repository,
            "change_record": change_record_repository
        },
        "services": {
            "opportunity": opportunity_service,
            "attachment": attachment_service
        }
    }

def create_sample_data(repositories):
    """Create sample data for the example."""
    # Create users
    sales_manager = User(
        name="John Doe",
        email="john.doe@example.com",
        role=UserRole.SALES_MANAGER,
        employee_id="EMP12345",
        department="Sales",
        job_title="Sales Manager"
    )
    repositories["user"].add(sales_manager)
    
    admin = User(
        name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        employee_id="EMP11111",
        department="IT",
        job_title="System Administrator"
    )
    repositories["user"].add(admin)
    
    # Create customers
    customer = Customer(
        name="Acme Inc.",
        industry="Technology",
        website="https://acme.example.com",
        description="A leading technology company",
        primary_contact_name="Jane Smith",
        primary_contact_email="jane.smith@acme.example.com",
        primary_contact_phone="555-123-4567"
    )
    repositories["customer"].add(customer)
    
    # Create skills
    aws_migration_skill = SkillsCatalog(
        name="AWS Migration",
        category=SkillType.TECHNICAL,
        description="Experience with migrating workloads to AWS",
        is_active=True
    )
    repositories["skills_catalog"].add(aws_migration_skill)
    
    cloud_architecture_skill = SkillsCatalog(
        name="Cloud Architecture",
        category=SkillType.TECHNICAL,
        description="Experience with designing cloud architectures",
        is_active=True
    )
    repositories["skills_catalog"].add(cloud_architecture_skill)
    
    presentation_skill = SkillsCatalog(
        name="Executive Presentation",
        category=SkillType.SOFT,
        description="Experience with presenting to executives",
        is_active=True
    )
    repositories["skills_catalog"].add(presentation_skill)
    
    return {
        "sales_manager": sales_manager,
        "admin": admin,
        "customer": customer,
        "skills": {
            "aws_migration": aws_migration_skill,
            "cloud_architecture": cloud_architecture_skill,
            "presentation": presentation_skill
        }
    }

def setup_event_listeners():
    """Set up event listeners for the example."""
    def on_opportunity_created(data):
        logger.info(f"Event: Opportunity created with ID {data['opportunity_id']}")
    
    def on_opportunity_submitted(data):
        logger.info(f"Event: Opportunity submitted with ID {data['opportunity_id']}")
    
    def on_opportunity_cancelled(data):
        logger.info(f"Event: Opportunity cancelled with ID {data['opportunity_id']}, reason: {data['reason']}")
    
    def on_opportunity_reactivated(data):
        logger.info(f"Event: Opportunity reactivated with ID {data['opportunity_id']}")
    
    EventPublisher.subscribe("opportunity.created", on_opportunity_created)
    EventPublisher.subscribe("opportunity.submitted", on_opportunity_submitted)
    EventPublisher.subscribe("opportunity.cancelled", on_opportunity_cancelled)
    EventPublisher.subscribe("opportunity.reactivated", on_opportunity_reactivated)

def run_example():
    """Run the example workflow."""
    # Set up repositories and services
    context = setup_repositories_and_services()
    repositories = context["repositories"]
    services = context["services"]
    
    # Set up event listeners
    setup_event_listeners()
    
    # Create sample data
    data = create_sample_data(repositories)
    
    # Example workflow: Create and manage an opportunity
    logger.info("=== Starting Example Workflow ===")
    
    # 1. Create an opportunity
    logger.info("1. Creating a new opportunity...")
    geographic_requirements = {
        "region_id": str(uuid.uuid4()),
        "name": "North America",
        "requires_physical_presence": True,
        "allows_remote_work": True
    }
    
    opportunity = services["opportunity"].create_opportunity(
        title="Cloud Migration Project",
        customer_id=data["customer"].id,
        customer_name=data["customer"].name,
        sales_manager_id=data["sales_manager"].id,
        description="Migrate on-premises infrastructure to the cloud",
        priority=Priority.HIGH,
        annual_recurring_revenue=100000.0,
        geographic_requirements=geographic_requirements
    )
    
    logger.info(f"Created opportunity: {opportunity.title} (ID: {opportunity.id})")
    
    # 2. Add a problem statement
    logger.info("2. Adding a problem statement...")
    problem_statement_content = """
    Acme Inc. is currently running their infrastructure on-premises and is facing scalability issues
    as their business grows. They need to migrate their workloads to AWS to improve scalability,
    reduce operational costs, and increase reliability. The migration needs to be done with minimal
    disruption to their business operations. They have a mix of legacy applications and modern
    microservices that need to be migrated.
    """
    
    problem_statement = services["opportunity"].add_problem_statement(
        opportunity_id=opportunity.id,
        content=problem_statement_content
    )
    
    logger.info(f"Added problem statement with {len(problem_statement.content)} characters")
    
    # 3. Add skill requirements
    logger.info("3. Adding skill requirements...")
    
    aws_migration_requirement = services["opportunity"].add_skill_requirement(
        opportunity_id=opportunity.id,
        skill_id=data["skills"]["aws_migration"].id,
        skill_type=SkillType.TECHNICAL,
        importance_level=ImportanceLevel.MUST_HAVE,
        minimum_proficiency_level=ProficiencyLevel.ADVANCED
    )
    
    cloud_architecture_requirement = services["opportunity"].add_skill_requirement(
        opportunity_id=opportunity.id,
        skill_id=data["skills"]["cloud_architecture"].id,
        skill_type=SkillType.TECHNICAL,
        importance_level=ImportanceLevel.MUST_HAVE,
        minimum_proficiency_level=ProficiencyLevel.EXPERT
    )
    
    presentation_requirement = services["opportunity"].add_skill_requirement(
        opportunity_id=opportunity.id,
        skill_id=data["skills"]["presentation"].id,
        skill_type=SkillType.SOFT,
        importance_level=ImportanceLevel.NICE_TO_HAVE,
        minimum_proficiency_level=ProficiencyLevel.INTERMEDIATE
    )
    
    logger.info(f"Added {3} skill requirements")
    
    # 4. Add timeline requirement
    logger.info("4. Adding timeline requirement...")
    
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
    specific_days = [
        (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
        (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
        (datetime.now() + timedelta(days=89)).strftime("%Y-%m-%d")
    ]
    
    timeline = services["opportunity"].add_timeline_requirement(
        opportunity_id=opportunity.id,
        start_date=start_date,
        end_date=end_date,
        is_flexible=False,
        specific_days=specific_days
    )
    
    logger.info(f"Added timeline requirement from {start_date} to {end_date}")
    
    # 5. Submit the opportunity
    logger.info("5. Submitting the opportunity...")
    
    submitted_opportunity = services["opportunity"].submit_opportunity(
        opportunity_id=opportunity.id,
        user_id=data["sales_manager"].id
    )
    
    logger.info(f"Submitted opportunity with status: {submitted_opportunity.status.value}")
    
    # 6. Cancel the opportunity
    logger.info("6. Cancelling the opportunity...")
    
    cancelled_opportunity = services["opportunity"].cancel_opportunity(
        opportunity_id=opportunity.id,
        user_id=data["sales_manager"].id,
        reason="Customer decided to postpone the project"
    )
    
    logger.info(f"Cancelled opportunity with status: {cancelled_opportunity.status.value}")
    
    # 7. Reactivate the opportunity
    logger.info("7. Reactivating the opportunity...")
    
    reactivated_opportunity = services["opportunity"].reactivate_opportunity(
        opportunity_id=opportunity.id,
        user_id=data["sales_manager"].id
    )
    
    logger.info(f"Reactivated opportunity with status: {reactivated_opportunity.status.value}")
    
    # 8. Get opportunity details
    logger.info("8. Getting opportunity details...")
    
    opportunity_details = services["opportunity"].get_opportunity_details(opportunity.id)
    
    logger.info(f"Retrieved opportunity details:")
    logger.info(f"  - Title: {opportunity_details['opportunity'].title}")
    logger.info(f"  - Status: {opportunity_details['opportunity'].status.value}")
    logger.info(f"  - Problem Statement: {len(opportunity_details['problem_statement'].content)} characters")
    logger.info(f"  - Skill Requirements: {len(opportunity_details['skill_requirements'])} requirements")
    logger.info(f"  - Timeline: {opportunity_details['timeline'].expected_start_date} to {opportunity_details['timeline'].expected_end_date}")
    logger.info(f"  - Status History: {len(opportunity_details['status_history'])} status changes")
    logger.info(f"  - Change History: {len(opportunity_details['change_history'])} changes")
    
    logger.info("=== Example Workflow Completed ===")

if __name__ == "__main__":
    run_example()
