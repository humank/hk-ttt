"""
SkillRequirement database model.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class SkillRequirement(Base):
    """SkillRequirement database model."""
    
    __tablename__ = "skill_requirements"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=False)
    skill_id = Column(String(36), nullable=False)
    skill_name = Column(String(100), nullable=False)
    skill_type = Column(String(20), nullable=False)  # TECHNICAL, SOFT, DOMAIN
    importance_level = Column(String(20), nullable=False)  # MUST_HAVE, NICE_TO_HAVE, PREFERRED
    minimum_proficiency_level = Column(String(20), nullable=False)  # BEGINNER, INTERMEDIATE, ADVANCED, EXPERT
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    opportunity = relationship("Opportunity", back_populates="skill_requirements")
    
    def __repr__(self):
        return f"<SkillRequirement(id={self.id}, skill_name='{self.skill_name}', importance='{self.importance_level}')>"
