"""
Skills validation service for skill requirements validation logic.
"""

from typing import List, Dict, Any, Set
import logging

from ..value_objects.skill_requirement import SkillRequirement
from ..enums.skill_importance import SkillImportance


class SkillsValidationService:
    """Service for validating skill requirements and business rules."""
    
    def __init__(self):
        """Initialize the skills validation service."""
        self.logger = logging.getLogger(__name__)
        
        # Predefined skill categories and common skills
        self.valid_categories = ["Technical", "Soft", "Industry"]
        self.common_technical_skills = {
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Python", "Java", 
            "JavaScript", "React", "Node.js", "SQL", "NoSQL", "MongoDB",
            "PostgreSQL", "Redis", "Elasticsearch", "Kafka", "RabbitMQ",
            "Terraform", "Ansible", "Jenkins", "GitLab CI", "GitHub Actions"
        }
        self.common_soft_skills = {
            "Communication", "Leadership", "Problem Solving", "Team Collaboration",
            "Project Management", "Analytical Thinking", "Creativity", "Adaptability",
            "Time Management", "Presentation Skills", "Mentoring", "Negotiation"
        }
        self.common_industry_skills = {
            "Financial Services", "Healthcare", "E-commerce", "Manufacturing",
            "Telecommunications", "Government", "Education", "Media & Entertainment",
            "Retail", "Automotive", "Energy", "Real Estate", "Insurance"
        }
    
    def validate_skill_requirement(self, skill_data: Dict[str, Any]) -> List[str]:
        """Validate individual skill requirement data."""
        errors = []
        
        # Skill name validation
        skill_name = skill_data.get('skill_name', '').strip()
        if not skill_name:
            errors.append("Skill name is required")
        
        # Category validation
        category = skill_data.get('skill_category', '').strip()
        if not category:
            errors.append("Skill category is required")
        elif category not in self.valid_categories:
            errors.append(f"Skill category must be one of: {self.valid_categories}")
        
        # Importance validation
        importance_str = skill_data.get('importance')
        if not importance_str:
            errors.append("Skill importance is required")
        else:
            try:
                SkillImportance.from_string(importance_str)
            except ValueError:
                errors.append(f"Invalid skill importance: {importance_str}")
        
        # Proficiency level validation
        proficiency = skill_data.get('proficiency_level')
        if proficiency:
            valid_levels = ["Beginner", "Intermediate", "Advanced", "Expert"]
            if proficiency not in valid_levels:
                errors.append(f"Proficiency level must be one of: {valid_levels}")
        
        return errors
    
    def validate_skill_requirements_collection(self, skill_requirements: List[SkillRequirement]) -> List[str]:
        """Validate a collection of skill requirements."""
        errors = []
        
        if not skill_requirements:
            errors.append("At least one skill requirement must be specified")
            return errors
        
        # Check for mandatory skills
        mandatory_skills = [skill for skill in skill_requirements if skill.is_mandatory]
        if not mandatory_skills:
            errors.append("At least one mandatory skill requirement must be specified")
        
        # Check for duplicates
        skill_keys = set()
        for skill in skill_requirements:
            key = (skill.skill_name.lower(), skill.skill_category)
            if key in skill_keys:
                errors.append(f"Duplicate skill requirement: {skill.skill_name} in {skill.skill_category}")
            skill_keys.add(key)
        
        # Validate skill distribution
        category_counts = {}
        for skill in skill_requirements:
            category_counts[skill.skill_category] = category_counts.get(skill.skill_category, 0) + 1
        
        # Business rule: Should have at least one technical skill
        if category_counts.get("Technical", 0) == 0:
            errors.append("At least one technical skill requirement should be specified")
        
        # Warning for too many skills
        if len(skill_requirements) > 15:
            errors.append("Too many skill requirements may limit architect availability")
        
        return errors
    
    def validate_skill_against_catalog(self, skill_name: str, category: str) -> Dict[str, Any]:
        """Validate skill against predefined skill catalog."""
        result = {
            "is_recognized": False,
            "suggestions": [],
            "category_match": True
        }
        
        # Get appropriate skill set based on category
        if category == "Technical":
            skill_set = self.common_technical_skills
        elif category == "Soft":
            skill_set = self.common_soft_skills
        elif category == "Industry":
            skill_set = self.common_industry_skills
        else:
            return result
        
        # Check exact match
        if skill_name in skill_set:
            result["is_recognized"] = True
            return result
        
        # Find similar skills (simple string matching)
        skill_lower = skill_name.lower()
        suggestions = []
        
        for known_skill in skill_set:
            if skill_lower in known_skill.lower() or known_skill.lower() in skill_lower:
                suggestions.append(known_skill)
        
        result["suggestions"] = suggestions[:5]  # Limit to 5 suggestions
        
        return result
    
    def get_skill_recommendations(self, skill_requirements: List[SkillRequirement]) -> List[str]:
        """Get recommendations for skill requirements optimization."""
        recommendations = []
        
        # Analyze current skills
        categories = {}
        importance_counts = {"Must Have": 0, "Nice to Have": 0}
        
        for skill in skill_requirements:
            categories[skill.skill_category] = categories.get(skill.skill_category, 0) + 1
            importance_counts[skill.importance.value] += 1
        
        # Category balance recommendations
        if categories.get("Technical", 0) > 10:
            recommendations.append("Consider reducing technical skills to improve architect matching")
        
        if categories.get("Soft", 0) == 0:
            recommendations.append("Consider adding soft skills for better team collaboration")
        
        # Importance balance recommendations
        if importance_counts["Must Have"] > 8:
            recommendations.append("Too many mandatory skills may limit available architects")
        
        if importance_counts["Nice to Have"] == 0:
            recommendations.append("Consider marking some skills as 'Nice to Have' for flexibility")
        
        # Specific skill recommendations
        technical_skills = [s.skill_name for s in skill_requirements if s.skill_category == "Technical"]
        
        if any("AWS" in skill for skill in technical_skills):
            if not any("Cloud Architecture" in skill for skill in technical_skills):
                recommendations.append("Consider adding 'Cloud Architecture' for AWS-related opportunities")
        
        return recommendations
    
    def calculate_skill_complexity_score(self, skill_requirements: List[SkillRequirement]) -> Dict[str, Any]:
        """Calculate complexity score for skill requirements."""
        score = 0
        factors = []
        
        # Base score from number of skills
        skill_count = len(skill_requirements)
        if skill_count <= 5:
            score += 20
        elif skill_count <= 10:
            score += 10
        else:
            score -= 10
            factors.append("High number of skills")
        
        # Mandatory skills factor
        mandatory_count = len([s for s in skill_requirements if s.is_mandatory])
        if mandatory_count <= 3:
            score += 15
        elif mandatory_count <= 6:
            score += 5
        else:
            score -= 15
            factors.append("Too many mandatory skills")
        
        # Proficiency level factor
        expert_skills = [s for s in skill_requirements if s.proficiency_level == "Expert"]
        if len(expert_skills) > 3:
            score -= 20
            factors.append("Multiple expert-level skills required")
        
        # Category diversity factor
        categories = set(s.skill_category for s in skill_requirements)
        if len(categories) >= 2:
            score += 10
            factors.append("Good skill category diversity")
        
        return {
            "score": max(0, min(100, score + 50)),  # Normalize to 0-100
            "factors": factors,
            "complexity": "Low" if score >= 70 else "Medium" if score >= 40 else "High",
            "matching_likelihood": "High" if score >= 70 else "Medium" if score >= 40 else "Low"
        }
    
    def suggest_skill_alternatives(self, skill_requirement: SkillRequirement) -> List[Dict[str, Any]]:
        """Suggest alternative skills that might increase matching opportunities."""
        alternatives = []
        
        skill_name = skill_requirement.skill_name.lower()
        
        # Technology alternatives
        tech_alternatives = {
            "aws": ["Azure", "Google Cloud Platform"],
            "azure": ["AWS", "Google Cloud Platform"],
            "react": ["Vue.js", "Angular"],
            "angular": ["React", "Vue.js"],
            "mysql": ["PostgreSQL", "SQL Server"],
            "mongodb": ["DynamoDB", "Cassandra"]
        }
        
        for tech, alts in tech_alternatives.items():
            if tech in skill_name:
                for alt in alts:
                    alternatives.append({
                        "skill_name": alt,
                        "reason": f"Alternative to {skill_requirement.skill_name}",
                        "category": skill_requirement.skill_category
                    })
        
        return alternatives
    
    def validate_skill_progression(self, skill_requirements: List[SkillRequirement]) -> List[str]:
        """Validate logical progression in skill requirements."""
        warnings = []
        
        # Check for conflicting proficiency levels
        skill_groups = {}
        for skill in skill_requirements:
            base_skill = skill.skill_name.split()[0].lower()  # Get base technology
            if base_skill not in skill_groups:
                skill_groups[base_skill] = []
            skill_groups[base_skill].append(skill)
        
        for base_skill, skills in skill_groups.items():
            if len(skills) > 1:
                proficiency_levels = [s.proficiency_level for s in skills if s.proficiency_level]
                if "Beginner" in proficiency_levels and "Expert" in proficiency_levels:
                    warnings.append(f"Conflicting proficiency levels for {base_skill}-related skills")
        
        return warnings
