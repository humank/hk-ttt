"""
Customer repository interface for data access abstraction.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from ...domain.entities.customer import Customer


class CustomerRepository(ABC):
    """Abstract base class for customer repository implementations."""
    
    @abstractmethod
    def save(self, customer: Customer) -> Customer:
        """Save a customer to the repository."""
        pass
    
    @abstractmethod
    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        """Find a customer by its ID."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Customer]:
        """Find all customers."""
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Customer]:
        """Find a customer by name (exact match)."""
        pass
    
    @abstractmethod
    def search_by_name(self, name_pattern: str) -> List[Customer]:
        """Search customers by name pattern (partial match)."""
        pass
    
    @abstractmethod
    def find_by_industry(self, industry: str) -> List[Customer]:
        """Find all customers in a specific industry."""
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Customer]:
        """Find a customer by email address."""
        pass
    
    @abstractmethod
    def search(self, criteria: Dict[str, Any]) -> List[Customer]:
        """Search customers based on multiple criteria."""
        pass
    
    @abstractmethod
    def delete(self, customer_id: str) -> bool:
        """Delete a customer from the repository."""
        pass
    
    @abstractmethod
    def exists(self, customer_id: str) -> bool:
        """Check if a customer exists in the repository."""
        pass
    
    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        """Check if a customer with the given name exists."""
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Check if a customer with the given email exists."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Get the total count of customers."""
        pass
    
    @abstractmethod
    def count_by_industry(self, industry: str) -> int:
        """Get count of customers by industry."""
        pass
    
    # Advanced query methods
    
    @abstractmethod
    def find_customers_with_opportunities(self) -> List[Customer]:
        """Find customers that have associated opportunities."""
        pass
    
    @abstractmethod
    def find_customers_without_contact_info(self) -> List[Customer]:
        """Find customers missing contact information."""
        pass
    
    @abstractmethod
    def get_industries(self) -> List[str]:
        """Get list of all unique industries."""
        pass
    
    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """Get repository statistics."""
        pass
