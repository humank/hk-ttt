"""
TimelineRequirement database model.
"""

from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class TimelineRequirement(Base):
    """TimelineRequirement database model."""
    
    __tablename__ = "timeline_requirements"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=False)
    start_date = Column(String(10), nullable=False)  # YYYY-MM-DD format
    end_date = Column(String(10), nullable=False)    # YYYY-MM-DD format
    is_flexible = Column(Boolean, nullable=False)
    specific_days = Column(JSON, nullable=True)  # List of specific days
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    opportunity = relationship("Opportunity", back_populates="timeline_requirement")
    
    def __repr__(self):
        return f"<TimelineRequirement(id={self.id}, start_date='{self.start_date}', end_date='{self.end_date}')>"
