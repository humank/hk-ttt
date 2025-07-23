"""
Opportunity database model.
"""

from sqlalchemy import Column, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Opportunity(Base):
    """Opportunity database model."""
    
    __tablename__ = "opportunities"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    customer_id = Column(String(36), nullable=False)
    customer_name = Column(String(100), nullable=False)
    sales_manager_id = Column(String(36), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(20), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    annual_recurring_revenue = Column(Float, nullable=False)
    geographic_requirements = Column(JSON, nullable=False)
    status = Column(String(20), nullable=False, default="DRAFT")  # DRAFT, SUBMITTED, CANCELLED, COMPLETED
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    reactivation_deadline = Column(DateTime, nullable=True)
    
    # Relationships
    problem_statement = relationship("ProblemStatement", back_populates="opportunity", uselist=False)
    skill_requirements = relationship("SkillRequirement", back_populates="opportunity")
    timeline_requirement = relationship("TimelineRequirement", back_populates="opportunity", uselist=False)
    status_history = relationship("OpportunityStatus", back_populates="opportunity")
    change_records = relationship("ChangeRecord", back_populates="opportunity")
    
    def __repr__(self):
        return f"<Opportunity(id={self.id}, title='{self.title}', status='{self.status}')>"
