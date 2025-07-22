"""
Test example demonstrating opportunity status transitions.
"""

import logging
from decimal import Decimal
from datetime import date, timedelta

# Import domain model components
from customer import Customer
from opportunity import Opportunity
from problem_statement import ProblemStatement
from skill_requirement import SkillRequirement
from timeline_specification import TimelineSpecification
from priority import Priority
from status import OpportunityStatus
from skill_importance import SkillImportance
from timeline_flexibility import TimelineFlexibility

# Import repositories
from in_memory_customer_repository import InMemoryCustomerRepository
from in_memory_opportunity_repository import InMemoryOpportunityRepository

# Import services
from opportunity_validation_service import OpportunityValidationService
from status_transition_service import StatusTransitionService
from opportunity_application_service import OpportunityApplicationService

# Import event handling
from event_dispatcher import get_event_dispatcher


def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_sample_opportunity():
    """Create a sample opportunity for testing."""
    # Setup repositories
    customer_repo = InMemoryCustomerRepository()
    opportunity_repo = InMemoryOpportunityRepository()
    
    # Create customer
    customer = Customer(
        name="Tech Solutions Inc",
        industry="Technology",
        contact_email="contact@techsolutions.com"
    )
    customer = customer_repo.save(customer)
    
    # Create opportunity
    opportunity = Opportunity(
        title="Digital Transformation Project",
        description="Complete digital transformation of legacy systems",
        customer_id=customer.id,
        sales_manager_id="sm_002",
        annual_recurring_revenue=Decimal("1200000"),
        priority=Priority.HIGH
    )
    
    # Add problem statement
    problem_statement = ProblemStatement(
        title="Legacy System Modernization",
        description="Client needs to modernize their legacy systems to improve efficiency and reduce costs. Current systems are outdated and causing operational challenges.",
        business_impact="Expected 60% cost reduction and improved operational efficiency",
        technical_requirements="Cloud migration, API development, data modernization",
        success_criteria="Successful migration with zero data loss and improved performance"
    )
    opportunity.set_problem_statement(problem_statement)
    
    # Add skill requirements
    skills = [
        SkillRequirement("Python", "Technical", SkillImportance.MUST_HAVE, "Advanced"),
        SkillRequirement("AWS", "Technical", SkillImportance.MUST_HAVE, "Intermediate"),
        SkillRequirement("Project Management", "Soft", SkillImportance.MUST_HAVE),
        SkillRequirement("Healthcare", "Industry", SkillImportance.NICE_TO_HAVE)
    ]
    
    for skill in skills:
        opportunity.add_skill_requirement(skill)
    
    # Set timeline
    timeline = TimelineSpecification(
        expected_start_date=date.today() + timedelta(days=45),
        expected_duration_days=180,
        flexibility=TimelineFlexibility.FLEXIBLE
    )
    opportunity.set_timeline_specification(timeline)
    
    # Save opportunity
    opportunity = opportunity_repo.save(opportunity)
    
    return opportunity_repo, customer_repo, opportunity


def test_status_transitions():
    """Test various status transitions."""
    print("=== Testing Status Transitions ===\n")
    
    # Setup
    opportunity_repo, customer_repo, opportunity = create_sample_opportunity()
    validation_service = OpportunityValidationService()
    status_transition_service = StatusTransitionService(validation_service)
    
    # Setup event dispatcher
    event_dispatcher = get_event_dispatcher()
    
    def log_status_event(event):
        print(f"📧 Status Event: {event.get_status_change_summary()}")
    
    event_dispatcher.register_function_handler("StatusChangedEvent", log_status_event)
    
    print(f"Initial opportunity status: {opportunity.status}")
    print(f"Opportunity ID: {opportunity.id}")
    
    try:
        # Test 1: Submit opportunity (Draft -> Submitted)
        print("\n1. Testing submission (Draft -> Submitted)...")
        result = status_transition_service.submit_opportunity(opportunity, "sm_002")
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"   Status: {opportunity.status}")
            print(f"   Next steps: {result['next_steps']}")
            opportunity_repo.save(opportunity)
        else:
            print(f"❌ Submission failed: {result['errors']}")
            return
        
        # Test 2: Start matching process (Submitted -> Matching in Progress)
        print("\n2. Testing matching start (Submitted -> Matching in Progress)...")
        result = status_transition_service.start_matching_process(opportunity, "system")
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"   Status: {opportunity.status}")
            print(f"   Estimated completion: {result['estimated_completion']}")
            opportunity_repo.save(opportunity)
        else:
            print(f"❌ Matching start failed: {result['errors']}")
        
        # Test 3: Complete matching with results (Matching in Progress -> Matches Found)
        print("\n3. Testing matching completion (Matching in Progress -> Matches Found)...")
        result = status_transition_service.complete_matching_process(
            opportunity, matches_found=True, completed_by="matching_engine", match_count=3
        )
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"   Status: {opportunity.status}")
            print(f"   Next steps: {result['next_steps']}")
            opportunity_repo.save(opportunity)
        else:
            print(f"❌ Matching completion failed: {result['errors']}")
        
        # Test 4: Select architect (Matches Found -> Architect Selected)
        print("\n4. Testing architect selection (Matches Found -> Architect Selected)...")
        result = status_transition_service.select_architect(
            opportunity, "arch_001", "sm_002", "Selected based on AWS expertise"
        )
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"   Status: {opportunity.status}")
            print(f"   Selected architect: {result['selected_architect_id']}")
            print(f"   Next steps: {result['next_steps']}")
            opportunity_repo.save(opportunity)
        else:
            print(f"❌ Architect selection failed: {result['errors']}")
        
        # Test 5: Complete opportunity (Architect Selected -> Completed)
        print("\n5. Testing opportunity completion (Architect Selected -> Completed)...")
        result = status_transition_service.complete_opportunity(
            opportunity, "sm_002", "Project completed successfully with all objectives met"
        )
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"   Status: {opportunity.status}")
            print(f"   Completion date: {result['completion_date']}")
            opportunity_repo.save(opportunity)
        else:
            print(f"❌ Completion failed: {result['errors']}")
        
        # Test 6: Show status history
        print("\n6. Status History:")
        for i, history in enumerate(opportunity.status_history, 1):
            from_status = history.from_status.value if history.from_status else "None"
            print(f"   {i}. {from_status} -> {history.to_status.value}")
            print(f"      Changed by: {history.changed_by}")
            print(f"      Reason: {history.change_reason}")
            print(f"      Date: {history.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if history.notes:
                print(f"      Notes: {history.notes}")
            print()
        
        print("✅ All status transitions completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during status transitions: {str(e)}")
        import traceback
        traceback.print_exc()


def test_invalid_transitions():
    """Test invalid status transitions."""
    print("\n=== Testing Invalid Status Transitions ===\n")
    
    # Setup
    opportunity_repo, customer_repo, opportunity = create_sample_opportunity()
    validation_service = OpportunityValidationService()
    status_transition_service = StatusTransitionService(validation_service)
    
    print(f"Current opportunity status: {opportunity.status}")
    
    # Test 1: Try to complete without architect selection
    print("\n1. Testing invalid completion (Draft -> Completed)...")
    result = status_transition_service.complete_opportunity(opportunity, "sm_002")
    if not result["success"]:
        print(f"✅ Correctly rejected invalid transition: {result['errors']}")
    else:
        print("❌ Should have rejected invalid transition")
    
    # Test 2: Try to select architect without matches
    print("\n2. Testing invalid architect selection (Draft -> Architect Selected)...")
    result = status_transition_service.select_architect(opportunity, "arch_001", "sm_002")
    if not result["success"]:
        print(f"✅ Correctly rejected invalid transition: {result['errors']}")
    else:
        print("❌ Should have rejected invalid transition")
    
    # Test 3: Get available transitions
    print("\n3. Available transitions from current status:")
    available_transitions = status_transition_service.get_available_transitions(opportunity)
    for transition in available_transitions:
        print(f"   - {transition['to_status']}: {transition['description']}")


def test_cancellation_and_reactivation():
    """Test opportunity cancellation and reactivation."""
    print("\n=== Testing Cancellation and Reactivation ===\n")
    
    # Setup
    opportunity_repo, customer_repo, opportunity = create_sample_opportunity()
    validation_service = OpportunityValidationService()
    status_transition_service = StatusTransitionService(validation_service)
    
    # Setup event dispatcher
    event_dispatcher = get_event_dispatcher()
    
    def log_cancellation_event(event):
        print(f"📧 Cancellation Event: Opportunity '{event.opportunity_title}' cancelled")
        print(f"   Reason: {event.cancellation_reason}")
        print(f"   Can be reactivated until: {event.reactivation_deadline}")
    
    event_dispatcher.register_function_handler("OpportunityCancelledEvent", log_cancellation_event)
    
    try:
        # Submit opportunity first
        status_transition_service.submit_opportunity(opportunity, "sm_002")
        opportunity_repo.save(opportunity)
        
        print(f"Current status: {opportunity.status}")
        
        # Test 1: Cancel opportunity
        print("\n1. Testing opportunity cancellation...")
        result = status_transition_service.cancel_opportunity(
            opportunity, "sm_002", "Client budget constraints", 
            "Client decided to postpone the project due to budget limitations"
        )
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"   Status: {opportunity.status}")
            print(f"   Cancellation date: {result['cancellation_date']}")
            print(f"   Reactivation deadline: {result['reactivation_deadline']}")
            opportunity_repo.save(opportunity)
        else:
            print(f"❌ Cancellation failed: {result['errors']}")
            return
        
        # Test 2: Reactivate opportunity
        print("\n2. Testing opportunity reactivation...")
        result = status_transition_service.reactivate_opportunity(
            opportunity, "sm_002", "Client budget approved, ready to proceed"
        )
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"   Status: {opportunity.status}")
            print(f"   Next steps: {result['next_steps']}")
            opportunity_repo.save(opportunity)
        else:
            print(f"❌ Reactivation failed: {result['errors']}")
        
        # Test 3: Try to reactivate again (should fail)
        print("\n3. Testing invalid reactivation...")
        result = status_transition_service.reactivate_opportunity(opportunity, "sm_002")
        if not result["success"]:
            print(f"✅ Correctly rejected invalid reactivation: {result['errors']}")
        else:
            print("❌ Should have rejected invalid reactivation")
        
        print("\n✅ Cancellation and reactivation tests completed!")
        
    except Exception as e:
        print(f"❌ Error during cancellation/reactivation: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    setup_logging()
    test_status_transitions()
    test_invalid_transitions()
    test_cancellation_and_reactivation()
