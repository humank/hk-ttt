"""
Test example demonstrating opportunity creation workflow.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import logging
from decimal import Decimal
from datetime import date, timedelta

# Import domain model components
from opportunity_management.domain.entities.customer import Customer
from opportunity_management.domain.entities.opportunity import Opportunity
from opportunity_management.domain.entities.problem_statement import ProblemStatement
from opportunity_management.domain.value_objects.skill_requirement import SkillRequirement
from opportunity_management.domain.value_objects.timeline_specification import TimelineSpecification
from opportunity_management.domain.value_objects.geographic_requirement import GeographicRequirement
from opportunity_management.domain.value_objects.language_requirement import LanguageRequirement, LanguageRequirements
from opportunity_management.domain.enums.priority import Priority
from opportunity_management.domain.enums.skill_importance import SkillImportance
from opportunity_management.domain.enums.timeline_flexibility import TimelineFlexibility

# Import repositories
from opportunity_management.infrastructure.repositories.in_memory_customer_repository import InMemoryCustomerRepository
from opportunity_management.infrastructure.repositories.in_memory_opportunity_repository import InMemoryOpportunityRepository

# Import services
from opportunity_management.domain.services.opportunity_validation_service import OpportunityValidationService
from opportunity_management.domain.services.status_transition_service import StatusTransitionService
from opportunity_management.domain.services.opportunity_modification_service import OpportunityModificationService
from opportunity_management.domain.services.skills_matching_preparation_service import SkillsMatchingPreparationService
from opportunity_management.application.services.opportunity_application_service import OpportunityApplicationService
from opportunity_management.application.queries.opportunity_query_service import OpportunityQueryService

# Import event handling
from opportunity_management.infrastructure.event_handling.event_dispatcher import get_event_dispatcher


def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def test_opportunity_creation_workflow():
    """Test the complete opportunity creation workflow."""
    print("=== Testing Opportunity Creation Workflow ===\n")
    
    # Setup repositories
    customer_repo = InMemoryCustomerRepository()
    opportunity_repo = InMemoryOpportunityRepository()
    
    # Setup services
    validation_service = OpportunityValidationService()
    status_transition_service = StatusTransitionService(validation_service)
    modification_service = OpportunityModificationService(validation_service)
    matching_preparation_service = SkillsMatchingPreparationService()
    
    # Setup application services
    app_service = OpportunityApplicationService(
        opportunity_repo, customer_repo, validation_service,
        status_transition_service, modification_service, matching_preparation_service
    )
    query_service = OpportunityQueryService(opportunity_repo, customer_repo)
    
    # Setup event dispatcher
    event_dispatcher = get_event_dispatcher()
    
    def log_event(event):
        print(f"📧 Event: {event}")
    
    # Register event handlers
    event_dispatcher.register_function_handler("OpportunityCreatedEvent", log_event)
    event_dispatcher.register_function_handler("StatusChangedEvent", log_event)
    
    try:
        # Step 1: Create a customer
        print("1. Creating customer...")
        customer = Customer(
            name="Acme Corporation",
            industry="Technology",
            contact_email="john.doe@acme.com",
            contact_phone="+1-555-0123",
            address="123 Tech Street, Silicon Valley, CA"
        )
        customer = customer_repo.save(customer)
        print(f"✅ Customer created: {customer.name} (ID: {customer.id})")
        
        # Step 2: Create opportunity
        print("\n2. Creating opportunity...")
        opportunity_data = {
            "title": "Cloud Migration Project",
            "description": "Migrate legacy systems to AWS cloud infrastructure",
            "customer_id": customer.id,
            "sales_manager_id": "sm_001",
            "annual_recurring_revenue": "750000",
            "priority": "High"
        }
        
        result = app_service.create_opportunity(opportunity_data)
        if result["success"]:
            opportunity_id = result["opportunity_id"]
            print(f"✅ Opportunity created: {opportunity_id}")
        else:
            print(f"❌ Failed to create opportunity: {result['errors']}")
            return
        
        # Step 3: Add problem statement
        print("\n3. Adding problem statement...")
        problem_data = {
            "title": "Legacy System Modernization",
            "description": "The client has multiple legacy systems running on outdated infrastructure that need to be modernized and migrated to cloud. Current systems are experiencing performance issues and high maintenance costs.",
            "business_impact": "Reducing operational costs by 40% and improving system reliability",
            "technical_requirements": "AWS cloud migration, microservices architecture, containerization",
            "success_criteria": "Zero downtime migration, 50% performance improvement, cost reduction",
            "constraints": "Must complete migration within 6 months, minimal business disruption"
        }
        
        result = app_service.add_problem_statement(opportunity_id, problem_data, "sm_001")
        if result["success"]:
            print(f"✅ Problem statement added (Complete: {result['is_complete']})")
        else:
            print(f"❌ Failed to add problem statement: {result['errors']}")
        
        # Step 4: Add skill requirements
        print("\n4. Adding skill requirements...")
        skills_data = [
            {
                "skill_name": "AWS",
                "skill_category": "Technical",
                "importance": "Must Have",
                "proficiency_level": "Advanced",
                "description": "AWS cloud services and architecture"
            },
            {
                "skill_name": "Docker",
                "skill_category": "Technical",
                "importance": "Must Have",
                "proficiency_level": "Intermediate",
                "description": "Containerization and orchestration"
            },
            {
                "skill_name": "Kubernetes",
                "skill_category": "Technical",
                "importance": "Nice to Have",
                "proficiency_level": "Intermediate",
                "description": "Container orchestration platform"
            },
            {
                "skill_name": "Communication",
                "skill_category": "Soft",
                "importance": "Must Have",
                "description": "Excellent communication skills for client interaction"
            },
            {
                "skill_name": "Financial Services",
                "skill_category": "Industry",
                "importance": "Nice to Have",
                "description": "Experience in financial services industry"
            }
        ]
        
        result = app_service.add_skill_requirements(opportunity_id, skills_data, "sm_001")
        if result["success"]:
            print(f"✅ Added {result['total_skills']} skill requirements ({result['mandatory_skills']} mandatory)")
        else:
            print(f"❌ Failed to add skills: {result['errors']}")
        
        # Step 5: Set timeline
        print("\n5. Setting timeline...")
        timeline_data = {
            "expected_start_date": (date.today() + timedelta(days=30)).isoformat(),
            "expected_duration_days": 120,
            "flexibility": "Flexible",
            "specific_days_required": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "notes": "Prefer to start after current project completion"
        }
        
        result = app_service.set_timeline(opportunity_id, timeline_data, "sm_001")
        if result["success"]:
            print("✅ Timeline set successfully")
        else:
            print(f"❌ Failed to set timeline: {result['errors']}")
        
        # Step 6: Submit opportunity
        print("\n6. Submitting opportunity for matching...")
        result = app_service.submit_opportunity(opportunity_id, "sm_001")
        if result["success"]:
            print(f"✅ Opportunity submitted: {result['message']}")
            print(f"   Next steps: {result['next_steps']}")
        else:
            print(f"❌ Failed to submit: {result['errors']}")
        
        # Step 7: Get opportunity details
        print("\n7. Retrieving opportunity details...")
        opportunity_details = query_service.get_opportunity_by_id(opportunity_id)
        if opportunity_details:
            print(f"✅ Opportunity Details:")
            print(f"   Title: {opportunity_details['title']}")
            print(f"   Status: {opportunity_details['status']}")
            print(f"   Priority: {opportunity_details['priority']}")
            print(f"   Customer: {opportunity_details['customer']['name']}")
            print(f"   ARR: ${opportunity_details['annual_recurring_revenue']}")
            print(f"   Skills: {len(opportunity_details['skill_requirements'])}")
            print(f"   Ready for matching: {opportunity_details.get('is_ready_for_matching', False)}")
        
        # Step 8: Get sales manager dashboard
        print("\n8. Getting sales manager dashboard...")
        dashboard = query_service.get_sales_manager_dashboard("sm_001")
        print(f"✅ Dashboard Summary:")
        print(f"   Total opportunities: {dashboard['summary']['total_opportunities']}")
        print(f"   Active opportunities: {dashboard['summary']['active_opportunities']}")
        print(f"   Total ARR: ${dashboard['summary']['total_arr']}")
        print(f"   By status: {dashboard['by_status']}")
        
        # Step 9: Prepare for matching
        print("\n9. Preparing for matching...")
        result = app_service.prepare_for_matching(opportunity_id)
        if result["success"]:
            print(f"✅ Prepared for matching (Readiness score: {result['readiness_score']})")
            matching_criteria = result['matching_criteria']
            print(f"   Mandatory skills: {len(matching_criteria['skills']['mandatory_skills'])}")
            print(f"   Optional skills: {len(matching_criteria['skills']['optional_skills'])}")
            print(f"   Minimum match score: {matching_criteria['minimum_match_score']}")
        else:
            print(f"❌ Not ready for matching: {result['errors']}")
        
        print("\n=== Opportunity Creation Workflow Completed Successfully! ===")
        
        # Display event history
        print("\n📧 Event History:")
        events = event_dispatcher.get_event_history()
        for event in events:
            print(f"   - {event['event_type']} at {event['occurred_at']}")
        
    except Exception as e:
        print(f"❌ Error during workflow: {str(e)}")
        import traceback
        traceback.print_exc()


def test_validation_scenarios():
    """Test various validation scenarios."""
    print("\n=== Testing Validation Scenarios ===\n")
    
    validation_service = OpportunityValidationService()
    
    # Test 1: Invalid opportunity data
    print("1. Testing invalid opportunity data...")
    invalid_data = {
        "title": "",  # Empty title
        "description": "Valid description",
        "customer_id": "cust_001",
        "sales_manager_id": "",  # Empty sales manager
        "annual_recurring_revenue": "-1000",  # Negative ARR
        "priority": "Invalid Priority"  # Invalid priority
    }
    
    errors = validation_service.validate_for_creation(invalid_data)
    if errors:
        print("✅ Validation correctly caught errors:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("❌ Validation should have caught errors")
    
    # Test 2: Valid opportunity data
    print("\n2. Testing valid opportunity data...")
    valid_data = {
        "title": "Valid Opportunity",
        "description": "This is a valid opportunity description",
        "customer_id": "cust_001",
        "sales_manager_id": "sm_001",
        "annual_recurring_revenue": "500000",
        "priority": "Medium"
    }
    
    errors = validation_service.validate_for_creation(valid_data)
    if not errors:
        print("✅ Valid data passed validation")
    else:
        print(f"❌ Valid data failed validation: {errors}")


if __name__ == "__main__":
    setup_logging()
    test_opportunity_creation_workflow()
    test_validation_scenarios()
