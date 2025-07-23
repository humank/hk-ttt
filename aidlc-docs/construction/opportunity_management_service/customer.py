"""
Customer entity for the Opportunity Management Service.
"""

import uuid
from dataclasses import dataclass, field
from typing import Optional, List

from .base_entity import BaseEntity

@dataclass
class Customer(BaseEntity):
    """Customer entity representing a client organization."""
    
    name: str
    industry: str
    website: Optional[str] = None
    description: Optional[str] = None
    primary_contact_name: Optional[str] = None
    primary_contact_email: Optional[str] = None
    primary_contact_phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True
    
    def update_contact_info(self, name: Optional[str] = None, email: Optional[str] = None,
                           phone: Optional[str] = None) -> None:
        """Update primary contact information."""
        if name:
            self.primary_contact_name = name
        if email:
            self.primary_contact_email = email
        if phone:
            self.primary_contact_phone = phone
        self.update()
    
    def deactivate(self) -> None:
        """Deactivate the customer."""
        self.is_active = False
        self.update()
    
    def activate(self) -> None:
        """Activate the customer."""
        self.is_active = True
        self.update()
