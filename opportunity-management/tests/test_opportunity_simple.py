"""
Simplified opportunity creation test.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from decimal import Decimal
from datetime import date, timedelta

def test_opportunity_creation():
    """Test creating opportunities with various configurations."""
    print("🧪 Testing Opportunity Creation")
    print("=" * 40)
    
    try:
        # Import required components
        from opportunity_management.domain.entities.customer import Customer
        from opportunity_management.domain.entities.opportunity import Opportunity
        from opportunity_management.domain.enums.priority import Priority
        from opportunity_management.domain.enums.status import OpportunityStatus
        from opportunity_management.domain.value_objects.skill_requirement import SkillRequirement
        from opportunity_management.domain.enums.skill_importance import SkillImportance
        
        print("✅ All imports successful")
        
        # Create a customer
        customer = Customer(
            name="TechCorp Solutions",
            industry="Technology",
            contact_email="contact@techcorp.com"
        )
        print(f"✅ Created customer: {customer.name} (ID: {customer.id})")
        
        # Create an opportunity
        opportunity = Opportunity(
            title="Cloud Migration Project",
            description="Migrate legacy systems to cloud infrastructure",
            customer_id=customer.id,
            sales_manager_id="sm_001",
            annual_recurring_revenue=Decimal("750000"),
            priority=Priority.HIGH
        )
        print(f"✅ Created opportunity: {opportunity.title} (ID: {opportunity.id})")
        print(f"   Priority: {opportunity.priority.value}")
        print(f"   Status: {opportunity.status.value}")
        print(f"   ARR: ${opportunity.annual_recurring_revenue:,}")
        
        # Test skill requirements
        skill_req = SkillRequirement(
            skill_name="Python Development",
            skill_category="Technical",
            importance=SkillImportance.MUST_HAVE,
            proficiency_level="Advanced"
        )
        print(f"✅ Created skill requirement: {skill_req.skill_name}")
        
        # Add skill to opportunity
        opportunity.add_skill_requirement(skill_req)
        print(f"✅ Added skill requirement to opportunity")
        print(f"   Skills count: {len(opportunity.skill_requirements)}")
        
        # Test status transitions
        print(f"✅ Current status: {opportunity.status.value}")
        print(f"   Can transition to SUBMITTED: {opportunity.status.can_transition_to(OpportunityStatus.SUBMITTED)}")
        print(f"   Can transition to COMPLETED: {opportunity.status.can_transition_to(OpportunityStatus.COMPLETED)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_priority_and_status_enums():
    """Test priority and status enum functionality."""
    print("\n🧪 Testing Enums")
    print("=" * 20)
    
    try:
        from opportunity_management.domain.enums.priority import Priority
        from opportunity_management.domain.enums.status import OpportunityStatus
        
        # Test Priority enum
        priorities = [Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.CRITICAL]
        print("✅ Priority levels:")
        for p in priorities:
            print(f"   {p.value} (weight: {p.weight})")
        
        # Test Status enum
        print("\n✅ Status transitions:")
        draft = OpportunityStatus.DRAFT
        print(f"   From {draft.value}:")
        for status in OpportunityStatus:
            if draft.can_transition_to(status):
                print(f"     → {status.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Running Opportunity Management Tests")
    print("=" * 50)
    
    tests = [
        test_priority_and_status_enums,
        test_opportunity_creation,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    main()
