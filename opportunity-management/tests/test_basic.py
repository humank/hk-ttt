"""
Basic tests to verify the domain model is working correctly.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from decimal import Decimal
from datetime import date, timedelta

def test_basic_imports():
    """Test that basic imports work."""
    try:
        from opportunity_management.domain.enums.priority import Priority
        from opportunity_management.domain.enums.status import OpportunityStatus
        from opportunity_management.domain.entities.customer import Customer
        from opportunity_management.domain.entities.opportunity import Opportunity
        print("✅ Basic imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_create_customer():
    """Test creating a customer."""
    try:
        from opportunity_management.domain.entities.customer import Customer
        
        customer = Customer(
            name="Test Company",
            industry="Technology",
            contact_email="test@company.com"
        )
        
        assert customer.name == "Test Company"
        assert customer.industry == "Technology"
        assert customer.contact_email == "test@company.com"
        assert customer.id is not None
        
        print("✅ Customer creation successful")
        return True
    except Exception as e:
        print(f"❌ Customer creation error: {e}")
        return False

def test_create_opportunity():
    """Test creating an opportunity."""
    try:
        from opportunity_management.domain.entities.customer import Customer
        from opportunity_management.domain.entities.opportunity import Opportunity
        from opportunity_management.domain.enums.priority import Priority
        
        # Create customer first
        customer = Customer(name="Test Company")
        
        # Create opportunity
        opportunity = Opportunity(
            title="Test Opportunity",
            description="This is a test opportunity",
            customer_id=customer.id,
            sales_manager_id="sm_001",
            annual_recurring_revenue=Decimal("500000"),
            priority=Priority.HIGH
        )
        
        assert opportunity.title == "Test Opportunity"
        assert opportunity.priority == Priority.HIGH
        assert opportunity.annual_recurring_revenue == Decimal("500000")
        assert opportunity.id is not None
        
        print("✅ Opportunity creation successful")
        return True
    except Exception as e:
        print(f"❌ Opportunity creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enums():
    """Test enum functionality."""
    try:
        from opportunity_management.domain.enums.priority import Priority
        from opportunity_management.domain.enums.status import OpportunityStatus
        
        # Test Priority enum
        assert Priority.HIGH.value == "High"
        assert Priority.HIGH.weight == 3
        
        # Test Status enum
        assert OpportunityStatus.DRAFT.value == "Draft"
        assert OpportunityStatus.DRAFT.can_transition_to(OpportunityStatus.SUBMITTED)
        assert not OpportunityStatus.DRAFT.can_transition_to(OpportunityStatus.COMPLETED)
        
        print("✅ Enum functionality successful")
        return True
    except Exception as e:
        print(f"❌ Enum test error: {e}")
        return False

def main():
    """Run all basic tests."""
    print("🧪 Running Basic Tests")
    print("=" * 30)
    
    tests = [
        test_basic_imports,
        test_enums,
        test_create_customer,
        test_create_opportunity,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    main()
