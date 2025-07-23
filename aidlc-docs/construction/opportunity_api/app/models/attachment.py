"""
Attachment database model.
"""

from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Attachment(Base):
    """Attachment database model."""
    
    __tablename__ = "attachments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    problem_statement_id = Column(String(36), ForeignKey("problem_statements.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_url = Column(String(500), nullable=False)
    uploaded_by = Column(String(36), nullable=False)
    uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_removed = Column(Boolean, nullable=False, default=False)
    
    # Relationships
    problem_statement = relationship("ProblemStatement", back_populates="attachments")
    
    def __repr__(self):
        return f"<Attachment(id={self.id}, file_name='{self.file_name}', is_removed={self.is_removed})>"
