"""
ChangeRecord database model.
"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class ChangeRecord(Base):
    """ChangeRecord database model."""
    
    __tablename__ = "change_records"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=False)
    changed_by = Column(String(36), nullable=False)
    field_changed = Column(String(100), nullable=False)
    reason = Column(Text, nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    changed_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    opportunity = relationship("Opportunity", back_populates="change_records")
    
    def __repr__(self):
        return f"<ChangeRecord(id={self.id}, field_changed='{self.field_changed}', changed_at='{self.changed_at}')>"
