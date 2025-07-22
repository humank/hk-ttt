"""
Comprehensive example demonstrating the complete opportunity management workflow.
This example shows how to use all the domain model components together.
"""

import logging
from decimal import Decimal
from datetime import date, timedelta

# Import all domain model components
from customer import Customer
from opportunity import Opportunity
from problem_statement import ProblemStatement
from skill_requirement import SkillRequirement
from timeline_specification import TimelineSpecification
from geographic_requirement import GeographicRequirement
from language_requirement import LanguageRequirement, LanguageRequirements
from document_attachment import DocumentAttachment
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
from opportunity_modification_service import OpportunityModificationService
from skills_matching_preparation_service import SkillsMatchingPreparationService
from opportunity_application_service import OpportunityApplicationService
from opportunity_query_service import OpportunityQueryService

# Import event handling
from event_dispatcher import get_event_dispatcher, EventHandler

# Import utilities
from date_utils import DateUtils
from validators import validate_required_string, validate_positive_decimal


def setup_logging():
    """Setup comprehensive logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('opportunity_management.log')
        ]
    )


class OpportunityEventHandler(EventHandler):
    """Custom event handler for opportunity events."""
    
    def handle(self, event):
        """Handle opportunity events."""
        if event.event_type == "OpportunityCreatedEvent":
            print(f"🎉 New Opportunity Created: {event.opportunity_title}")
            if event.is_high_value:
                print("   💰 High-value opportunity detected!")
            if event.is_high_priority:
                print("   🚨 High-priority opportunity!")
        
        elif event.event_type == "StatusChangedEvent":
            print(f"📊 Status Update: {event.get_status_change_summary()}")
            if event.requires_notification:
                recipients = event.get_notification_recipients()
                print(f"   📧 Notifications sent to: {recipients}")
        
        elif event.event_type == "OpportunityModifiedEvent":
            print(f"✏️  Opportunity Modified: {event.opportunity_title}")
            if event.is_significant_change:
                print("   ⚠️  Significant changes detected")
        
        elif event.event_type == "OpportunityCancelledEvent":
            print(f"❌ Opportunity Cancelled: {event.opportunity_title}")
            impact = event.get_impact_assessment()
            print(f"   Impact severity: {impact['severity']}")
    
    def can_handle(self, event_type: str) -> bool:
        """Check if this handler can handle the event type."""
        return event_type in [
            "OpportunityCreatedEvent", "StatusChangedEvent", 
            "OpportunityModifiedEvent", "OpportunityCancelledEvent"
        ]


def setup_services():
    """Setup all services and dependencies."""
    print("🔧 Setting up services and dependencies...")
    
    # Repositories
    customer_repo = InMemoryCustomerRepository()
    opportunity_repo = InMemoryOpportunityRepository()
    
    # Domain services
    validation_service = OpportunityValidationService()
    status_transition_service = StatusTransitionService(validation_service)
    modification_service = OpportunityModificationService(validation_service)
    matching_preparation_service = SkillsMatchingPreparationService()
    
    # Application services
    app_service = OpportunityApplicationService(
        opportunity_repo, customer_repo, validation_service,
        status_transition_service, modification_service, matching_preparation_service
    )
    query_service = OpportunityQueryService(opportunity_repo, customer_repo)
    
    # Event handling
    event_dispatcher = get_event_dispatcher()
    event_handler = OpportunityEventHandler()
    
    # Register event handlers
    event_dispatcher.register_handler("OpportunityCreatedEvent", event_handler)
    event_dispatcher.register_handler("StatusChangedEvent", event_handler)
    event_dispatcher.register_handler("OpportunityModifiedEvent", event_handler)
    event_dispatcher.register_handler("OpportunityCancelledEvent", event_handler)
    
    print("✅ Services setup completed!")
    
    return {
        'customer_repo': customer_repo,
        'opportunity_repo': opportunity_repo,
        'app_service': app_service,
        'query_service': query_service,
        'event_dispatcher': event_dispatcher
    }


def create_sample_customers(customer_repo):
    """Create sample customers for demonstration."""
    print("\n👥 Creating sample customers...")
    
    customers = [
        Customer(
            name="TechCorp Solutions",
            industry="Technology",
            contact_email="projects@techcorp.com",
            contact_phone="+1-555-0100",
            address="100 Innovation Drive, San Francisco, CA"
        ),
        Customer(
            name="Global Finance Inc",
            industry="Financial Services",
            contact_email="it@globalfinance.com",
            contact_phone="+1-555-0200",
            address="200 Wall Street, New York, NY"
        ),
        Customer(
            name="HealthTech Innovations",
            industry="Healthcare",
            contact_email="development@healthtech.com",
            contact_phone="+1-555-0300",
            address="300 Medical Center Blvd, Boston, MA"
        )
    ]
    
    saved_customers = []
    for customer in customers:
        saved_customer = customer_repo.save(customer)
        saved_customers.append(saved_customer)
        print(f"✅ Created customer: {customer.name} (ID: {customer.id})")
    
    return saved_customers


def demonstrate_opportunity_lifecycle(services, customers):
    """Demonstrate the complete opportunity lifecycle."""
    print("\n🔄 Demonstrating Complete Opportunity Lifecycle")
    print("=" * 60)
    
    app_service = services['app_service']
    query_service = services['query_service']
    
    # Step 1: Create Opportunity
    print("\n📝 Step 1: Creating Opportunity")
    opportunity_data = {
        "title": "Enterprise Cloud Migration",
        "description": "Comprehensive migration of legacy systems to modern cloud infrastructure with microservices architecture",
        "customer_id": customers[0].id,
        "sales_manager_id": "sm_001",
        "annual_recurring_revenue": "1500000",
        "priority": "Critical"
    }
    
    result = app_service.create_opportunity(opportunity_data)
    if not result["success"]:
        print(f"❌ Failed to create opportunity: {result['errors']}")
        return None
    
    opportunity_id = result["opportunity_id"]
    print(f"✅ Opportunity created with ID: {opportunity_id}")
    
    # Step 2: Add Problem Statement
    print("\n📋 Step 2: Adding Problem Statement")
    problem_data = {
        "title": "Legacy System Modernization Challenge",
        "description": "The client operates multiple legacy systems built over 15 years that are becoming increasingly difficult and expensive to maintain. These systems lack modern security features, have poor performance, and cannot scale to meet growing business demands. The infrastructure is primarily on-premises with limited disaster recovery capabilities.",
        "business_impact": "Current systems cost $2M annually in maintenance. Migration expected to reduce costs by 60% while improving performance by 300% and enabling new business capabilities worth $5M in additional revenue.",
        "technical_requirements": "Cloud-native architecture using AWS, containerized microservices, API-first design, automated CI/CD pipelines, comprehensive monitoring and logging, disaster recovery with RPO < 1 hour.",
        "success_criteria": "Zero-downtime migration, 99.9% uptime SLA, sub-second response times, automated scaling, comprehensive security compliance (SOC2, ISO27001), full disaster recovery capability.",
        "constraints": "Migration must be completed in 8 months, minimal business disruption during business hours, compliance with financial regulations, budget cap of $3M."
    }
    
    result = app_service.add_problem_statement(opportunity_id, problem_data, "sm_001")
    if result["success"]:
        print(f"✅ Problem statement added (Complete: {result['is_complete']})")
    else:
        print(f"❌ Failed to add problem statement: {result['errors']}")
    
    # Step 3: Add Comprehensive Skills Requirements
    print("\n🎯 Step 3: Adding Skills Requirements")
    skills_data = [
        # Technical Skills - Must Have
        {
            "skill_name": "AWS",
            "skill_category": "Technical",
            "importance": "Must Have",
            "proficiency_level": "Expert",
            "description": "AWS cloud services, architecture patterns, and best practices"
        },
        {
            "skill_name": "Docker",
            "skill_category": "Technical",
            "importance": "Must Have",
            "proficiency_level": "Advanced",
            "description": "Containerization and container orchestration"
        },
        {
            "skill_name": "Kubernetes",
            "skill_category": "Technical",
            "importance": "Must Have",
            "proficiency_level": "Advanced",
            "description": "Container orchestration and cluster management"
        },
        {
            "skill_name": "Terraform",
            "skill_category": "Technical",
            "importance": "Must Have",
            "proficiency_level": "Intermediate",
            "description": "Infrastructure as Code for AWS resources"
        },
        {
            "skill_name": "Python",
            "skill_category": "Technical",
            "importance": "Must Have",
            "proficiency_level": "Advanced",
            "description": "Backend development and automation scripting"
        },
        # Technical Skills - Nice to Have
        {
            "skill_name": "Java",
            "skill_category": "Technical",
            "importance": "Nice to Have",
            "proficiency_level": "Intermediate",
            "description": "Legacy system integration and microservices development"
        },
        {
            "skill_name": "React",
            "skill_category": "Technical",
            "importance": "Nice to Have",
            "proficiency_level": "Intermediate",
            "description": "Frontend modernization"
        },
        # Soft Skills
        {
            "skill_name": "Leadership",
            "skill_category": "Soft",
            "importance": "Must Have",
            "description": "Technical leadership and team coordination"
        },
        {
            "skill_name": "Communication",
            "skill_category": "Soft",
            "importance": "Must Have",
            "description": "Client communication and stakeholder management"
        },
        {
            "skill_name": "Problem Solving",
            "skill_category": "Soft",
            "importance": "Must Have",
            "description": "Complex technical problem resolution"
        },
        # Industry Knowledge
        {
            "skill_name": "Financial Services",
            "skill_category": "Industry",
            "importance": "Nice to Have",
            "description": "Understanding of financial regulations and compliance"
        }
    ]
    
    result = app_service.add_skill_requirements(opportunity_id, skills_data, "sm_001")
    if result["success"]:
        print(f"✅ Added {result['total_skills']} skills ({result['mandatory_skills']} mandatory)")
    else:
        print(f"❌ Failed to add skills: {result['errors']}")
    
    # Step 4: Set Timeline
    print("\n📅 Step 4: Setting Timeline")
    timeline_data = {
        "expected_start_date": (date.today() + timedelta(days=45)).isoformat(),
        "expected_duration_days": 240,  # 8 months
        "flexibility": "Negotiable",
        "specific_days_required": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "notes": "Prefer to start after Q1 planning cycle. Some flexibility on start date but duration is fixed due to regulatory deadlines."
    }
    
    result = app_service.set_timeline(opportunity_id, timeline_data, "sm_001")
    if result["success"]:
        print("✅ Timeline set successfully")
    else:
        print(f"❌ Failed to set timeline: {result['errors']}")
    
    # Step 5: Submit for Matching
    print("\n🎯 Step 5: Submitting for Matching")
    result = app_service.submit_opportunity(opportunity_id, "sm_001")
    if result["success"]:
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Submission failed: {result['errors']}")
    
    # Step 6: Simulate Matching Process
    print("\n🔍 Step 6: Simulating Matching Process")
    opportunity = services['opportunity_repo'].find_by_id(opportunity_id)
    status_service = services['app_service'].status_transition_service
    
    # Start matching
    result = status_service.start_matching_process(opportunity, "matching_system")
    if result["success"]:
        print(f"✅ Matching started: {result['message']}")
        services['opportunity_repo'].save(opportunity)
    
    # Complete matching with results
    result = status_service.complete_matching_process(
        opportunity, matches_found=True, completed_by="matching_system", match_count=5
    )
    if result["success"]:
        print(f"✅ Matching completed: {result['message']}")
        services['opportunity_repo'].save(opportunity)
    
    # Step 7: Select Architect
    print("\n👨‍💻 Step 7: Selecting Solution Architect")
    result = status_service.select_architect(
        opportunity, "arch_senior_001", "sm_001", 
        "Selected John Smith - 8 years AWS experience, led 3 similar migrations"
    )
    if result["success"]:
        print(f"✅ Architect selected: {result['selected_architect_id']}")
        services['opportunity_repo'].save(opportunity)
    
    # Step 8: Demonstrate Modification (Limited after architect selection)
    print("\n✏️  Step 8: Attempting Modification After Architect Selection")
    modification_data = {
        "priority": "Critical",  # This should be allowed
        "title": "New Title"     # This should be rejected
    }
    
    result = services['app_service'].modification_service.update_basic_information(
        opportunity, modification_data, "sm_001"
    )
    
    if result["success"]:
        print(f"✅ Allowed modifications: {result['changes_made']}")
    else:
        print(f"⚠️  Some modifications rejected: {result['errors']}")
    
    # Step 9: Complete Opportunity
    print("\n🎉 Step 9: Completing Opportunity")
    result = status_service.complete_opportunity(
        opportunity, "sm_001", 
        "Migration completed successfully. All systems migrated with zero downtime. Performance improved by 350% and costs reduced by 65%."
    )
    if result["success"]:
        print(f"✅ Opportunity completed: {result['message']}")
        services['opportunity_repo'].save(opportunity)
    
    return opportunity_id


def demonstrate_dashboard_and_reporting(services, opportunity_id):
    """Demonstrate dashboard and reporting capabilities."""
    print("\n📊 Dashboard and Reporting Demonstration")
    print("=" * 50)
    
    query_service = services['query_service']
    
    # Sales Manager Dashboard
    print("\n📈 Sales Manager Dashboard:")
    dashboard = query_service.get_sales_manager_dashboard("sm_001")
    
    print(f"Summary:")
    print(f"  Total Opportunities: {dashboard['summary']['total_opportunities']}")
    print(f"  Active Opportunities: {dashboard['summary']['active_opportunities']}")
    print(f"  Total ARR: ${dashboard['summary']['total_arr']:,.2f}")
    print(f"  Active ARR: ${dashboard['summary']['active_arr']:,.2f}")
    
    print(f"\nBy Status:")
    for status, count in dashboard['by_status'].items():
        if count > 0:
            print(f"  {status}: {count}")
    
    print(f"\nBy Priority:")
    for priority, count in dashboard['by_priority'].items():
        if count > 0:
            print(f"  {priority}: {count}")
    
    if dashboard['requiring_attention']:
        print(f"\n⚠️  Requiring Attention:")
        for item in dashboard['requiring_attention']:
            print(f"  - {item['reason']} (Age: {item['age_days']} days)")
    
    # Opportunity Details
    print(f"\n📋 Opportunity Details:")
    opportunity_details = query_service.get_opportunity_by_id(opportunity_id)
    if opportunity_details:
        print(f"  Title: {opportunity_details['title']}")
        print(f"  Status: {opportunity_details['status']}")
        print(f"  Customer: {opportunity_details['customer']['name']}")
        print(f"  Priority: {opportunity_details['priority']}")
        print(f"  ARR: ${opportunity_details['annual_recurring_revenue']}")
        print(f"  Skills Count: {len(opportunity_details['skill_requirements'])}")
        
        if opportunity_details.get('selected_architect_id'):
            print(f"  Selected Architect: {opportunity_details['selected_architect_id']}")
        
        if opportunity_details.get('completion_date'):
            print(f"  Completed: {opportunity_details['completion_date']}")
    
    # System Statistics
    print(f"\n📊 System Statistics:")
    stats = query_service.get_opportunity_statistics()
    print(f"  Total Opportunities: {stats['total_opportunities']}")
    print(f"  This Month: {stats['this_month_count']}")
    print(f"  Last Month: {stats['last_month_count']}")
    print(f"  Month-over-Month Change: {stats['month_over_month_change']:+d}")
    print(f"  Ready for Matching: {stats['ready_for_matching']}")
    print(f"  High Value Opportunities: {stats['high_value_count']}")
    print(f"  Average ARR: ${stats['average_arr']:,.2f}")


def demonstrate_advanced_features(services, customers):
    """Demonstrate advanced features like cloning, cancellation, etc."""
    print("\n🚀 Advanced Features Demonstration")
    print("=" * 40)
    
    app_service = services['app_service']
    
    # Create another opportunity for advanced features demo
    print("\n📝 Creating opportunity for advanced features demo...")
    opportunity_data = {
        "title": "AI-Powered Analytics Platform",
        "description": "Development of advanced analytics platform with machine learning capabilities",
        "customer_id": customers[1].id,
        "sales_manager_id": "sm_002",
        "annual_recurring_revenue": "800000",
        "priority": "High"
    }
    
    result = app_service.create_opportunity(opportunity_data)
    if not result["success"]:
        print(f"❌ Failed to create opportunity: {result['errors']}")
        return
    
    opportunity_id = result["opportunity_id"]
    print(f"✅ Created opportunity: {opportunity_id}")
    
    # Add minimal requirements
    problem_data = {
        "title": "Analytics Platform Development",
        "description": "Need to build a comprehensive analytics platform with AI/ML capabilities for real-time data processing and insights generation."
    }
    app_service.add_problem_statement(opportunity_id, problem_data, "sm_002")
    
    skills_data = [
        {
            "skill_name": "Python",
            "skill_category": "Technical",
            "importance": "Must Have",
            "proficiency_level": "Advanced"
        },
        {
            "skill_name": "Machine Learning",
            "skill_category": "Technical",
            "importance": "Must Have",
            "proficiency_level": "Intermediate"
        }
    ]
    app_service.add_skill_requirements(opportunity_id, skills_data, "sm_002")
    
    # Demonstrate Cloning
    print("\n🔄 Demonstrating Opportunity Cloning...")
    result = app_service.clone_opportunity(
        opportunity_id, "AI Analytics Platform - Phase 2", "sm_002"
    )
    if result["success"]:
        print(f"✅ Cloned opportunity: {result['cloned_id']}")
        print(f"   Original: {result['original_id']}")
    
    # Demonstrate Cancellation
    print("\n❌ Demonstrating Opportunity Cancellation...")
    result = app_service.cancel_opportunity(
        opportunity_id, "Budget constraints - project postponed", "sm_002",
        "Client decided to postpone due to budget reallocation for Q1"
    )
    if result["success"]:
        print(f"✅ Opportunity cancelled")
        print(f"   Reactivation deadline: {result['reactivation_deadline']}")
    
    # Demonstrate Reactivation
    print("\n🔄 Demonstrating Opportunity Reactivation...")
    result = app_service.reactivate_opportunity(
        opportunity_id, "sm_002", "Budget approved - ready to proceed"
    )
    if result["success"]:
        print(f"✅ Opportunity reactivated")
        print(f"   Status: Draft (ready for updates)")


def demonstrate_event_system(services):
    """Demonstrate the event system capabilities."""
    print("\n📧 Event System Demonstration")
    print("=" * 35)
    
    event_dispatcher = services['event_dispatcher']
    
    # Show event statistics
    stats = event_dispatcher.get_statistics()
    print(f"Event Statistics:")
    print(f"  Total Events Dispatched: {stats['total_events_dispatched']}")
    print(f"  Registered Handler Types: {stats['registered_handler_types']}")
    print(f"  Total Handlers: {stats['total_handlers']}")
    
    if stats['event_type_counts']:
        print(f"\nEvent Type Counts:")
        for event_type, count in stats['event_type_counts'].items():
            print(f"  {event_type}: {count}")
    
    # Show recent events
    print(f"\n📋 Recent Events:")
    recent_events = event_dispatcher.get_event_history(limit=10)
    for event in recent_events:
        print(f"  {event['occurred_at']}: {event['event_type']}")


def main():
    """Main demonstration function."""
    print("🎯 Opportunity Management System - Complete Demonstration")
    print("=" * 65)
    
    # Setup
    setup_logging()
    services = setup_services()
    customers = create_sample_customers(services['customer_repo'])
    
    try:
        # Main workflow demonstration
        opportunity_id = demonstrate_opportunity_lifecycle(services, customers)
        
        if opportunity_id:
            # Dashboard and reporting
            demonstrate_dashboard_and_reporting(services, opportunity_id)
            
            # Advanced features
            demonstrate_advanced_features(services, customers)
            
            # Event system
            demonstrate_event_system(services)
        
        print("\n🎉 Demonstration Completed Successfully!")
        print("\nKey Features Demonstrated:")
        print("✅ Complete opportunity lifecycle management")
        print("✅ Comprehensive skills requirements handling")
        print("✅ Status transitions with business rules")
        print("✅ Event-driven architecture")
        print("✅ Dashboard and reporting capabilities")
        print("✅ Advanced features (cloning, cancellation, reactivation)")
        print("✅ Validation and business rule enforcement")
        print("✅ In-memory repository implementation")
        print("✅ Domain-driven design patterns")
        
        # Show final repository statistics
        print(f"\n📊 Final Statistics:")
        customer_stats = services['customer_repo'].get_statistics()
        opportunity_stats = services['opportunity_repo'].get_statistics()
        
        print(f"Customers: {customer_stats['total_customers']}")
        print(f"Opportunities: {opportunity_stats['total_opportunities']}")
        print(f"Total ARR: ${opportunity_stats['total_arr']:,.2f}")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
