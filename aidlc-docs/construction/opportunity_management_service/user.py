"""
User entity for the Opportunity Management Service.
"""

import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class User:
    """User entity representing basic user information across the system."""
    
    name: str
    email: str
    role: str  # UserRole enum as string
    employee_id: str
    department: str
    job_title: str
    is_active: bool = True
    last_login_at: Optional[datetime] = None
    profile_picture_url: Optional[str] = None
    phone_number: Optional[str] = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def update(self) -> None:
        """Update the entity's last modified timestamp."""
        self.updated_at = datetime.now()
    
    def login(self) -> None:
        """Record a user login."""
        self.last_login_at = datetime.now()
        self.update()
    
    def deactivate(self) -> None:
        """Deactivate the user."""
        self.is_active = False
        self.update()
    
    def activate(self) -> None:
        """Activate the user."""
        self.is_active = True
        self.update()
    
    def update_profile(self, name: Optional[str] = None, email: Optional[str] = None,
                      department: Optional[str] = None, job_title: Optional[str] = None,
                      profile_picture_url: Optional[str] = None, phone_number: Optional[str] = None) -> None:
        """Update user profile information."""
        if name:
            self.name = name
        if email:
            self.email = email
        if department:
            self.department = department
        if job_title:
            self.job_title = job_title
        if profile_picture_url:
            self.profile_picture_url = profile_picture_url
        if phone_number:
            self.phone_number = phone_number
        self.update()
    
    def is_sales_manager(self) -> bool:
        """Check if the user is a Sales Manager."""
        return self.role == "SalesManager" and self.is_active
    
    def is_solution_architect(self) -> bool:
        """Check if the user is a Solution Architect."""
        return self.role == "SolutionArchitect" and self.is_active
    
    def is_admin(self) -> bool:
        """Check if the user is an Admin."""
        return self.role == "Admin" and self.is_active
    
    def __eq__(self, other):
        """Entities are equal if their IDs are equal."""
        if not isinstance(other, User):
            return False
        return self.id == other.id
    
    def __hash__(self):
        """Hash based on the entity's ID."""
        return hash(self.id)
