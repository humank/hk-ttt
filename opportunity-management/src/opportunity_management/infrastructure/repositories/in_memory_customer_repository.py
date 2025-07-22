"""
In-memory implementation of the customer repository.
"""

from typing import List, Optional, Dict, Any
import logging

from .customer_repository import CustomerRepository
from ...domain.entities.customer import Customer


class InMemoryCustomerRepository(CustomerRepository):
    """In-memory implementation of customer repository using dictionaries."""
    
    def __init__(self):
        """Initialize the in-memory repository."""
        self._customers: Dict[str, Customer] = {}
        self.logger = logging.getLogger(__name__)
    
    def save(self, customer: Customer) -> Customer:
        """Save a customer to the repository."""
        self.logger.debug(f"Saving customer {customer.id}")
        
        # Update timestamp if this is an existing customer
        if customer.id in self._customers:
            customer.update_timestamp()
        
        self._customers[customer.id] = customer
        return customer
    
    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        """Find a customer by its ID."""
        return self._customers.get(customer_id)
    
    def find_all(self) -> List[Customer]:
        """Find all customers."""
        return list(self._customers.values())
    
    def find_by_name(self, name: str) -> Optional[Customer]:
        """Find a customer by name (exact match)."""
        for customer in self._customers.values():
            if customer.name.lower() == name.lower():
                return customer
        return None
    
    def search_by_name(self, name_pattern: str) -> List[Customer]:
        """Search customers by name pattern (partial match)."""
        name_pattern_lower = name_pattern.lower()
        return [
            customer for customer in self._customers.values()
            if name_pattern_lower in customer.name.lower()
        ]
    
    def find_by_industry(self, industry: str) -> List[Customer]:
        """Find all customers in a specific industry."""
        return [
            customer for customer in self._customers.values()
            if customer.industry and customer.industry.lower() == industry.lower()
        ]
    
    def find_by_email(self, email: str) -> Optional[Customer]:
        """Find a customer by email address."""
        for customer in self._customers.values():
            if customer.contact_email and customer.contact_email.lower() == email.lower():
                return customer
        return None
    
    def search(self, criteria: Dict[str, Any]) -> List[Customer]:
        """Search customers based on multiple criteria."""
        results = list(self._customers.values())
        
        # Filter by name (partial match)
        if 'name_contains' in criteria:
            name_pattern = criteria['name_contains'].lower()
            results = [customer for customer in results 
                      if name_pattern in customer.name.lower()]
        
        # Filter by industry
        if 'industry' in criteria:
            industry = criteria['industry'].lower()
            results = [customer for customer in results 
                      if customer.industry and customer.industry.lower() == industry]
        
        # Filter by email domain
        if 'email_domain' in criteria:
            domain = criteria['email_domain'].lower()
            results = [customer for customer in results 
                      if customer.contact_email and domain in customer.contact_email.lower()]
        
        # Filter by has contact info
        if 'has_contact_info' in criteria:
            has_contact = criteria['has_contact_info']
            results = [customer for customer in results 
                      if customer.has_contact_info == has_contact]
        
        # Filter by creation date range
        if 'created_after' in criteria:
            from datetime import datetime
            created_after = datetime.fromisoformat(criteria['created_after'])
            results = [customer for customer in results 
                      if customer.created_at >= created_after]
        
        if 'created_before' in criteria:
            from datetime import datetime
            created_before = datetime.fromisoformat(criteria['created_before'])
            results = [customer for customer in results 
                      if customer.created_at <= created_before]
        
        return results
    
    def delete(self, customer_id: str) -> bool:
        """Delete a customer from the repository."""
        if customer_id in self._customers:
            del self._customers[customer_id]
            self.logger.debug(f"Deleted customer {customer_id}")
            return True
        return False
    
    def exists(self, customer_id: str) -> bool:
        """Check if a customer exists in the repository."""
        return customer_id in self._customers
    
    def exists_by_name(self, name: str) -> bool:
        """Check if a customer with the given name exists."""
        return self.find_by_name(name) is not None
    
    def exists_by_email(self, email: str) -> bool:
        """Check if a customer with the given email exists."""
        return self.find_by_email(email) is not None
    
    def count(self) -> int:
        """Get the total count of customers."""
        return len(self._customers)
    
    def count_by_industry(self, industry: str) -> int:
        """Get count of customers by industry."""
        return len(self.find_by_industry(industry))
    
    # Advanced query methods
    
    def find_customers_with_opportunities(self) -> List[Customer]:
        """Find customers that have associated opportunities."""
        # Note: This would typically require a join with opportunities
        # For now, we'll return all customers as we don't have the relationship
        # In a real implementation, this would query the opportunity repository
        return list(self._customers.values())
    
    def find_customers_without_contact_info(self) -> List[Customer]:
        """Find customers missing contact information."""
        return [
            customer for customer in self._customers.values()
            if not customer.has_contact_info
        ]
    
    def get_industries(self) -> List[str]:
        """Get list of all unique industries."""
        industries = set()
        for customer in self._customers.values():
            if customer.industry:
                industries.add(customer.industry)
        return sorted(list(industries))
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get repository statistics."""
        total_count = len(self._customers)
        
        if total_count == 0:
            return {
                "total_customers": 0,
                "by_industry": {},
                "with_contact_info": 0,
                "without_contact_info": 0,
                "unique_industries": 0
            }
        
        # Count by industry
        industry_counts = {}
        for industry in self.get_industries():
            industry_counts[industry] = self.count_by_industry(industry)
        
        # Count with/without contact info
        with_contact = len([c for c in self._customers.values() if c.has_contact_info])
        without_contact = total_count - with_contact
        
        return {
            "total_customers": total_count,
            "by_industry": industry_counts,
            "with_contact_info": with_contact,
            "without_contact_info": without_contact,
            "unique_industries": len(industry_counts)
        }
    
    def clear(self) -> None:
        """Clear all customers from the repository (for testing)."""
        self._customers.clear()
        self.logger.debug("Cleared all customers from repository")
    
    def bulk_save(self, customers: List[Customer]) -> List[Customer]:
        """Save multiple customers at once."""
        saved_customers = []
        for customer in customers:
            saved_customers.append(self.save(customer))
        return saved_customers
    
    def find_or_create_by_name(self, name: str, **kwargs) -> Customer:
        """Find customer by name or create new one if not found."""
        existing_customer = self.find_by_name(name)
        if existing_customer:
            return existing_customer
        
        # Create new customer
        new_customer = Customer(
            name=name,
            industry=kwargs.get('industry'),
            contact_email=kwargs.get('contact_email'),
            contact_phone=kwargs.get('contact_phone'),
            address=kwargs.get('address'),
            notes=kwargs.get('notes')
        )
        
        return self.save(new_customer)
