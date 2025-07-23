"""
OpportunityStatus database model.
"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class OpportunityStatus(Base):
    """OpportunityStatus database model."""
    
    __tablename__ = "opportunity_statuses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=False)
    status = Column(String(20), nullable=False)  # DRAFT, SUBMITTED, CANCELLED, COMPLETED
    changed_by = Column(String(36), nullable=False)
    reason = Column(Text, nullable=False)
    changed_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    opportunity = relationship("Opportunity", back_populates="status_history")
    
    def __repr__(self):
        return f"<OpportunityStatus(id={self.id}, status='{self.status}', changed_at='{self.changed_at}')>"
