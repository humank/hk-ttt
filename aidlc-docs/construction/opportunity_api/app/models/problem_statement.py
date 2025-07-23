"""
ProblemStatement database model.
"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class ProblemStatement(Base):
    """ProblemStatement database model."""
    
    __tablename__ = "problem_statements"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    opportunity = relationship("Opportunity", back_populates="problem_statement")
    attachments = relationship("Attachment", back_populates="problem_statement")
    
    def __repr__(self):
        return f"<ProblemStatement(id={self.id}, opportunity_id={self.opportunity_id})>"
