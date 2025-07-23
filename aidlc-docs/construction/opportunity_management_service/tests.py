"""
Unit tests for the Opportunity Management Service.
"""

import unittest
import uuid
from datetime import datetime, timedelta

from opportunity_management_service.user import User

class TestUser(unittest.TestCase):
    """Test cases for User entity."""
    
    def test_create_user(self):
        """Test creating a user."""
        user = User(
            name="John Doe",
            email="john.doe@example.com",
            role="SalesManager",
            employee_id="EMP12345",
            department="Sales",
            job_title="Sales Manager"
        )
        
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.role, "SalesManager")
        self.assertEqual(user.employee_id, "EMP12345")
        self.assertEqual(user.department, "Sales")
        self.assertEqual(user.job_title, "Sales Manager")
        self.assertTrue(user.is_active)
        self.assertIsNone(user.last_login_at)
    
    def test_user_login(self):
        """Test user login."""
        user = User(
            name="John Doe",
            email="john.doe@example.com",
            role="SalesManager",
            employee_id="EMP12345",
            department="Sales",
            job_title="Sales Manager"
        )
        
        self.assertIsNone(user.last_login_at)
        
        user.login()
        
        self.assertIsNotNone(user.last_login_at)
    
    def test_user_role_checks(self):
        """Test user role check methods."""
        sales_manager = User(
            name="John Doe",
            email="john.doe@example.com",
            role="SalesManager",
            employee_id="EMP12345",
            department="Sales",
            job_title="Sales Manager"
        )
        
        solution_architect = User(
            name="Jane Smith",
            email="jane.smith@example.com",
            role="SolutionArchitect",
            employee_id="EMP67890",
            department="Solutions",
            job_title="Solution Architect"
        )
        
        admin = User(
            name="Admin User",
            email="admin@example.com",
            role="Admin",
            employee_id="EMP11111",
            department="IT",
            job_title="System Administrator"
        )
        
        self.assertTrue(sales_manager.is_sales_manager())
        self.assertFalse(sales_manager.is_solution_architect())
        self.assertFalse(sales_manager.is_admin())
        
        self.assertFalse(solution_architect.is_sales_manager())
        self.assertTrue(solution_architect.is_solution_architect())
        self.assertFalse(solution_architect.is_admin())
        
        self.assertFalse(admin.is_sales_manager())
        self.assertFalse(admin.is_solution_architect())
        self.assertTrue(admin.is_admin())

if __name__ == '__main__':
    unittest.main()
