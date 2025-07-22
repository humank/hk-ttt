"""
Customer entity for opportunity management.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from .base_entity import BaseEntity


@dataclass
class Customer(BaseEntity):
    """Entity representing a customer in the opportunity management system."""
    
    name: str = ""
    industry: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    
    def __post_init__(self):
        """Validate customer after initialization."""
        super().__post_init__()
        
        if not self.name or not self.name.strip():
            raise ValueError("Customer name cannot be empty")
        
        if self.contact_email and not self._is_valid_email(self.contact_email):
            raise ValueError("Invalid email format")
    
    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def update_contact_info(self, email: Optional[str] = None, 
                           phone: Optional[str] = None, 
                           address: Optional[str] = None) -> None:
        """Update customer contact information."""
        if email is not None:
            if email and not self._is_valid_email(email):
                raise ValueError("Invalid email format")
            self.contact_email = email
        
        if phone is not None:
            self.contact_phone = phone
        
        if address is not None:
            self.address = address
        
        self.update_timestamp()
    
    def update_industry(self, industry: str) -> None:
        """Update customer industry."""
        self.industry = industry
        self.update_timestamp()
    
    def add_notes(self, notes: str) -> None:
        """Add or update customer notes."""
        if self.notes:
            self.notes += f"\n{notes}"
        else:
            self.notes = notes
        self.update_timestamp()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert customer to dictionary representation."""
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name,
            "industry": self.industry,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "address": self.address,
            "notes": self.notes
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Customer':
        """Create Customer from dictionary."""
        customer = cls(
            name=data["name"],
            industry=data.get("industry"),
            contact_email=data.get("contact_email"),
            contact_phone=data.get("contact_phone"),
            address=data.get("address"),
            notes=data.get("notes")
        )
        customer.update_from_dict(data)
        return customer
    
    @property
    def has_contact_info(self) -> bool:
        """Check if customer has any contact information."""
        return bool(self.contact_email or self.contact_phone or self.address)
    
    def __str__(self) -> str:
        """String representation of customer."""
        return f"Customer(id={self.id}, name={self.name})"
