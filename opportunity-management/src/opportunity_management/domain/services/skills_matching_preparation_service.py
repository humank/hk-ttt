"""
Skills matching preparation service for preparing opportunity data for the matching engine.
"""

from typing import List, Dict, Any, Set, Tuple
import logging

from ..entities.opportunity import Opportunity
from ..value_objects.skill_requirement import SkillRequirement
from ..enums.skill_importance import SkillImportance


class SkillsMatchingPreparationService:
    """Service for preparing skill requirements for the matching engine."""
    
    def __init__(self):
        """Initialize the skills matching preparation service."""
        self.logger = logging.getLogger(__name__)
        
        # Skill synonyms and related skills for better matching
        self.skill_synonyms = {
            "javascript": ["js", "ecmascript"],
            "python": ["py"],
            "aws": ["amazon web services"],
            "azure": ["microsoft azure"],
            "gcp": ["google cloud platform", "google cloud"],
            "kubernetes": ["k8s"],
            "docker": ["containerization"],
            "postgresql": ["postgres"],
            "mongodb": ["mongo"]
        }
        
        # Skill categories and their weights for matching
        self.category_weights = {
            "Technical": 0.6,
            "Soft": 0.2,
            "Industry": 0.2
        }
    
    def prepare_matching_criteria(self, opportunity: Opportunity) -> Dict[str, Any]:
        """Prepare comprehensive matching criteria for an opportunity."""
        self.logger.info(f"Preparing matching criteria for opportunity {opportunity.id}")
        
        if not opportunity.is_ready_for_matching:
            raise ValueError("Opportunity is not ready for matching")
        
        # Prepare skill requirements
        skill_criteria = self._prepare_skill_criteria(opportunity.skill_requirements)
        
        # Prepare timeline criteria
        timeline_criteria = self._prepare_timeline_criteria(opportunity)
        
        # Prepare geographic criteria
        geographic_criteria = self._prepare_geographic_criteria(opportunity)
        
        # Prepare language criteria
        language_criteria = self._prepare_language_criteria(opportunity)
        
        # Calculate overall matching weights
        matching_weights = self._calculate_matching_weights(opportunity)
        
        criteria = {
            "opportunity_id": opportunity.id,
            "opportunity_title": opportunity.title,
            "priority": opportunity.priority.value,
            "priority_weight": opportunity.priority.weight,
            "annual_recurring_revenue": str(opportunity.annual_recurring_revenue),
            "skills": skill_criteria,
            "timeline": timeline_criteria,
            "geographic": geographic_criteria,
            "languages": language_criteria,
            "matching_weights": matching_weights,
            "minimum_match_score": self._calculate_minimum_match_score(opportunity)
        }
        
        self.logger.info(f"Matching criteria prepared for opportunity {opportunity.id}")
        return criteria
    
    def _prepare_skill_criteria(self, skill_requirements: List[SkillRequirement]) -> Dict[str, Any]:
        """Prepare skill-based matching criteria."""
        mandatory_skills = []
        optional_skills = []
        skill_categories = {"Technical": [], "Soft": [], "Industry": []}
        
        for skill in skill_requirements:
            skill_data = {
                "name": skill.skill_name,
                "category": skill.skill_category,
                "importance": skill.importance.value,
                "weight": skill.importance.weight,
                "proficiency_level": skill.proficiency_level,
                "synonyms": self._get_skill_synonyms(skill.skill_name),
                "description": skill.description
            }
            
            if skill.is_mandatory:
                mandatory_skills.append(skill_data)
            else:
                optional_skills.append(skill_data)
            
            skill_categories[skill.skill_category].append(skill_data)
        
        return {
            "mandatory_skills": mandatory_skills,
            "optional_skills": optional_skills,
            "by_category": skill_categories,
            "total_skills": len(skill_requirements),
            "mandatory_count": len(mandatory_skills),
            "optional_count": len(optional_skills)
        }
    
    def _prepare_timeline_criteria(self, opportunity: Opportunity) -> Dict[str, Any]:
        """Prepare timeline-based matching criteria."""
        if not opportunity.timeline_specification:
            return {}
        
        timeline = opportunity.timeline_specification
        
        return {
            "start_date": timeline.expected_start_date.isoformat(),
            "duration_days": timeline.expected_duration_days,
            "end_date": timeline.calculated_end_date.isoformat(),
            "flexibility": timeline.flexibility.value,
            "allows_adjustment": timeline.flexibility.allows_adjustment,
            "specific_days": timeline.specific_days_required,
            "notes": timeline.notes,
            "urgency_score": self._calculate_urgency_score(timeline)
        }
    
    def _prepare_geographic_criteria(self, opportunity: Opportunity) -> Dict[str, Any]:
        """Prepare geographic-based matching criteria."""
        if not opportunity.geographic_requirement:
            return {"remote_allowed": True, "travel_required": False}
        
        geo = opportunity.geographic_requirement
        
        return {
            "preferred_locations": geo.preferred_locations,
            "remote_allowed": geo.remote_work_allowed,
            "travel_required": geo.travel_required,
            "travel_percentage": geo.travel_percentage,
            "time_zone_preference": geo.time_zone_preference,
            "country_restrictions": geo.country_restrictions,
            "location_flexibility": geo.is_location_flexible,
            "notes": geo.notes
        }
    
    def _prepare_language_criteria(self, opportunity: Opportunity) -> Dict[str, Any]:
        """Prepare language-based matching criteria."""
        if not opportunity.language_requirements:
            return {"required": False}
        
        lang_reqs = opportunity.language_requirements
        
        return {
            "required": True,
            "mandatory_languages": [
                {
                    "language": req.language,
                    "proficiency": req.proficiency_level,
                    "context": req.context
                }
                for req in lang_reqs.get_mandatory_languages()
            ],
            "optional_languages": [
                {
                    "language": req.language,
                    "proficiency": req.proficiency_level,
                    "context": req.context
                }
                for req in lang_reqs.get_optional_languages()
            ]
        }
    
    def _calculate_matching_weights(self, opportunity: Opportunity) -> Dict[str, float]:
        """Calculate weights for different matching criteria."""
        weights = {
            "skills": 0.5,
            "timeline": 0.2,
            "geographic": 0.15,
            "languages": 0.1,
            "priority_bonus": 0.05
        }
        
        # Adjust weights based on opportunity characteristics
        if opportunity.priority.weight >= 3:  # High or Critical priority
            weights["skills"] = 0.6
            weights["timeline"] = 0.25
        
        if opportunity.language_requirements:
            weights["languages"] = 0.15
            weights["skills"] = 0.45
        
        if (opportunity.geographic_requirement and 
            not opportunity.geographic_requirement.remote_work_allowed):
            weights["geographic"] = 0.25
            weights["skills"] = 0.45
        
        return weights
    
    def _calculate_minimum_match_score(self, opportunity: Opportunity) -> float:
        """Calculate minimum match score required for this opportunity."""
        base_score = 60.0  # Base minimum score
        
        # Adjust based on priority
        if opportunity.priority.weight >= 4:  # Critical
            base_score = 80.0
        elif opportunity.priority.weight >= 3:  # High
            base_score = 70.0
        
        # Adjust based on mandatory skills count
        mandatory_skills_count = len(opportunity.mandatory_skills)
        if mandatory_skills_count > 5:
            base_score += 5.0  # Higher bar for complex requirements
        
        # Adjust based on ARR
        from decimal import Decimal
        if opportunity.annual_recurring_revenue > Decimal('500000'):
            base_score += 5.0  # Higher bar for high-value opportunities
        
        return min(base_score, 90.0)  # Cap at 90%
    
    def _calculate_urgency_score(self, timeline_spec) -> int:
        """Calculate urgency score based on timeline."""
        from datetime import date
        
        days_until_start = (timeline_spec.expected_start_date - date.today()).days
        
        if days_until_start <= 7:
            return 10  # Very urgent
        elif days_until_start <= 14:
            return 8   # Urgent
        elif days_until_start <= 30:
            return 6   # Moderate
        elif days_until_start <= 60:
            return 4   # Normal
        else:
            return 2   # Low urgency
    
    def _get_skill_synonyms(self, skill_name: str) -> List[str]:
        """Get synonyms for a skill to improve matching."""
        skill_lower = skill_name.lower()
        
        # Direct lookup
        if skill_lower in self.skill_synonyms:
            return self.skill_synonyms[skill_lower]
        
        # Reverse lookup
        for main_skill, synonyms in self.skill_synonyms.items():
            if skill_lower in synonyms:
                return [main_skill] + [s for s in synonyms if s != skill_lower]
        
        return []
    
    def generate_matching_query(self, opportunity: Opportunity) -> Dict[str, Any]:
        """Generate a structured query for the matching engine."""
        criteria = self.prepare_matching_criteria(opportunity)
        
        # Create a structured query that the matching engine can use
        query = {
            "opportunity_id": opportunity.id,
            "query_type": "architect_matching",
            "filters": {
                "mandatory_skills": [
                    skill["name"] for skill in criteria["skills"]["mandatory_skills"]
                ],
                "skill_categories": list(criteria["skills"]["by_category"].keys()),
                "timeline_start": criteria["timeline"].get("start_date"),
                "timeline_end": criteria["timeline"].get("end_date"),
                "remote_work": criteria["geographic"].get("remote_allowed", True),
                "travel_required": criteria["geographic"].get("travel_required", False)
            },
            "scoring": {
                "weights": criteria["matching_weights"],
                "minimum_score": criteria["minimum_match_score"]
            },
            "preferences": {
                "preferred_locations": criteria["geographic"].get("preferred_locations", []),
                "optional_skills": [
                    skill["name"] for skill in criteria["skills"]["optional_skills"]
                ],
                "languages": criteria["languages"]
            }
        }
        
        return query
    
    def validate_matching_readiness(self, opportunity: Opportunity) -> Dict[str, Any]:
        """Validate if opportunity is ready for matching process."""
        issues = []
        warnings = []
        
        # Check mandatory requirements
        if not opportunity.skill_requirements:
            issues.append("No skill requirements specified")
        elif not opportunity.mandatory_skills:
            issues.append("No mandatory skills specified")
        
        if not opportunity.timeline_specification:
            issues.append("Timeline specification missing")
        
        if not opportunity.problem_statement:
            issues.append("Problem statement missing")
        elif not opportunity.problem_statement.is_complete:
            warnings.append("Problem statement is not complete")
        
        # Check for potential matching challenges
        if len(opportunity.mandatory_skills) > 8:
            warnings.append("High number of mandatory skills may limit matches")
        
        if (opportunity.timeline_specification and 
            opportunity.timeline_specification.total_duration_days < 14):
            warnings.append("Short timeline may limit architect availability")
        
        return {
            "is_ready": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "readiness_score": max(0, 100 - len(issues) * 25 - len(warnings) * 5)
        }
