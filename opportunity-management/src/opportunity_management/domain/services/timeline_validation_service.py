"""
Timeline validation service for timeline-related business logic.
"""

from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta
import logging

from ..value_objects.timeline_specification import TimelineSpecification
from ..enums.timeline_flexibility import TimelineFlexibility


class TimelineValidationService:
    """Service for validating timeline specifications and business rules."""
    
    def __init__(self):
        """Initialize the timeline validation service."""
        self.logger = logging.getLogger(__name__)
    
    def validate_timeline_specification(self, timeline_data: Dict[str, Any]) -> List[str]:
        """Validate timeline specification data."""
        errors = []
        
        # Start date validation
        start_date_str = timeline_data.get('expected_start_date')
        if not start_date_str:
            errors.append("Expected start date is required")
        else:
            try:
                start_date = date.fromisoformat(start_date_str)
                if start_date < date.today():
                    errors.append("Expected start date cannot be in the past")
            except ValueError:
                errors.append("Invalid start date format")
        
        # Duration validation
        duration = timeline_data.get('expected_duration_days')
        if not duration:
            errors.append("Expected duration is required")
        elif not isinstance(duration, int) or duration <= 0:
            errors.append("Expected duration must be a positive integer")
        
        # End date validation (if provided)
        end_date_str = timeline_data.get('expected_end_date')
        if end_date_str:
            try:
                end_date = date.fromisoformat(end_date_str)
                start_date = date.fromisoformat(start_date_str)
                if end_date <= start_date:
                    errors.append("Expected end date must be after start date")
            except ValueError:
                errors.append("Invalid end date format")
        
        # Flexibility validation
        flexibility_str = timeline_data.get('flexibility')
        if flexibility_str:
            try:
                TimelineFlexibility.from_string(flexibility_str)
            except ValueError:
                errors.append(f"Invalid timeline flexibility: {flexibility_str}")
        
        # Specific days validation
        specific_days = timeline_data.get('specific_days_required')
        if specific_days:
            valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            for day in specific_days:
                if day not in valid_days:
                    errors.append(f"Invalid day specified: {day}")
        
        return errors
    
    def validate_timeline_feasibility(self, timeline_spec: TimelineSpecification) -> List[str]:
        """Validate if timeline is feasible from business perspective."""
        errors = []
        
        # Check for unrealistic short timelines
        if timeline_spec.total_duration_days < 7:
            errors.append("Timeline duration should be at least 7 days for proper engagement")
        
        # Check for unrealistic long timelines
        if timeline_spec.total_duration_days > 365:
            errors.append("Timeline duration exceeds maximum allowed period of 365 days")
        
        # Weekend-only requirements validation
        if timeline_spec.specific_days_required:
            weekend_days = ["Saturday", "Sunday"]
            if all(day in weekend_days for day in timeline_spec.specific_days_required):
                errors.append("Weekend-only requirements may limit architect availability")
        
        # Holiday period validation
        if self._is_holiday_period(timeline_spec.expected_start_date):
            errors.append("Start date falls during holiday period - consider flexibility")
        
        return errors
    
    def validate_timeline_conflicts(self, timeline_spec: TimelineSpecification, 
                                  existing_timelines: List[TimelineSpecification]) -> List[str]:
        """Validate timeline against existing commitments."""
        errors = []
        
        conflicts = []
        for existing_timeline in existing_timelines:
            if timeline_spec.overlaps_with(existing_timeline):
                conflicts.append(existing_timeline)
        
        if conflicts:
            errors.append(f"Timeline conflicts with {len(conflicts)} existing commitment(s)")
        
        return errors
    
    def validate_timeline_modification(self, current_timeline: TimelineSpecification,
                                     new_timeline_data: Dict[str, Any],
                                     opportunity_status: str) -> List[str]:
        """Validate timeline modification based on opportunity status."""
        errors = []
        
        # Check if timeline can be modified based on status
        if opportunity_status in ["ARCHITECT_SELECTED", "COMPLETED"]:
            if not current_timeline.flexibility.allows_adjustment:
                errors.append("Timeline cannot be modified for fixed timelines after architect selection")
        
        # Validate new timeline data
        timeline_errors = self.validate_timeline_specification(new_timeline_data)
        errors.extend(timeline_errors)
        
        # Check for significant changes
        if 'expected_start_date' in new_timeline_data:
            try:
                new_start_date = date.fromisoformat(new_timeline_data['expected_start_date'])
                days_difference = abs((new_start_date - current_timeline.expected_start_date).days)
                
                if days_difference > 30:
                    errors.append("Start date change exceeds 30 days - may require stakeholder approval")
            except ValueError:
                pass  # Already caught in timeline specification validation
        
        return errors
    
    def get_timeline_recommendations(self, timeline_spec: TimelineSpecification) -> List[str]:
        """Get recommendations for timeline optimization."""
        recommendations = []
        
        # Duration recommendations
        if timeline_spec.total_duration_days < 14:
            recommendations.append("Consider extending timeline to at least 14 days for better outcomes")
        
        # Flexibility recommendations
        if timeline_spec.flexibility == TimelineFlexibility.FIXED:
            recommendations.append("Consider flexible timeline to increase architect availability")
        
        # Start date recommendations
        if timeline_spec.expected_start_date < date.today() + timedelta(days=7):
            recommendations.append("Consider starting at least 7 days from now for better preparation")
        
        # Specific days recommendations
        if timeline_spec.specific_days_required:
            weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            if not any(day in weekdays for day in timeline_spec.specific_days_required):
                recommendations.append("Including weekdays may increase architect availability")
        
        return recommendations
    
    def calculate_timeline_score(self, timeline_spec: TimelineSpecification) -> Dict[str, Any]:
        """Calculate a timeline feasibility score."""
        score = 100
        factors = []
        
        # Duration factor
        if timeline_spec.total_duration_days < 7:
            score -= 20
            factors.append("Very short duration")
        elif timeline_spec.total_duration_days > 180:
            score -= 10
            factors.append("Very long duration")
        
        # Flexibility factor
        if timeline_spec.flexibility == TimelineFlexibility.FIXED:
            score -= 15
            factors.append("Fixed timeline")
        elif timeline_spec.flexibility == TimelineFlexibility.FLEXIBLE:
            score += 10
            factors.append("Flexible timeline")
        
        # Start date factor
        days_until_start = (timeline_spec.expected_start_date - date.today()).days
        if days_until_start < 7:
            score -= 15
            factors.append("Very short notice")
        elif days_until_start > 90:
            score -= 5
            factors.append("Far future start")
        
        # Holiday factor
        if self._is_holiday_period(timeline_spec.expected_start_date):
            score -= 10
            factors.append("Holiday period start")
        
        return {
            "score": max(0, score),
            "factors": factors,
            "feasibility": "High" if score >= 80 else "Medium" if score >= 60 else "Low"
        }
    
    def _is_holiday_period(self, check_date: date) -> bool:
        """Check if date falls during common holiday periods."""
        # Simple holiday period detection (can be enhanced)
        month = check_date.month
        day = check_date.day
        
        # Christmas/New Year period
        if (month == 12 and day >= 20) or (month == 1 and day <= 5):
            return True
        
        # Summer vacation period (July-August)
        if month in [7, 8]:
            return True
        
        return False
    
    def get_available_time_slots(self, preferred_start: date, duration_days: int,
                               flexibility: TimelineFlexibility) -> List[Dict[str, Any]]:
        """Get available time slots based on preferences."""
        slots = []
        
        if flexibility == TimelineFlexibility.FIXED:
            # Only return the exact requested slot
            slots.append({
                "start_date": preferred_start.isoformat(),
                "end_date": (preferred_start + timedelta(days=duration_days)).isoformat(),
                "match_score": 100
            })
        else:
            # Return multiple options with different start dates
            for offset in [-7, 0, 7, 14]:
                start_date = preferred_start + timedelta(days=offset)
                if start_date >= date.today():
                    match_score = 100 - abs(offset)
                    slots.append({
                        "start_date": start_date.isoformat(),
                        "end_date": (start_date + timedelta(days=duration_days)).isoformat(),
                        "match_score": match_score
                    })
        
        return sorted(slots, key=lambda x: x["match_score"], reverse=True)
