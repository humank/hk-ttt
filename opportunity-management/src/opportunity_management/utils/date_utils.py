"""
Date and time utilities for the opportunity management system.
"""

from datetime import date, datetime, timedelta
from typing import List, Optional, Tuple
import calendar


class DateUtils:
    """Utility class for date and time operations."""
    
    @staticmethod
    def is_business_day(check_date: date) -> bool:
        """Check if date is a business day (Monday-Friday)."""
        return check_date.weekday() < 5
    
    @staticmethod
    def is_weekend(check_date: date) -> bool:
        """Check if date is a weekend (Saturday-Sunday)."""
        return check_date.weekday() >= 5
    
    @staticmethod
    def next_business_day(start_date: date) -> date:
        """Get the next business day after the given date."""
        next_day = start_date + timedelta(days=1)
        while not DateUtils.is_business_day(next_day):
            next_day += timedelta(days=1)
        return next_day
    
    @staticmethod
    def previous_business_day(start_date: date) -> date:
        """Get the previous business day before the given date."""
        prev_day = start_date - timedelta(days=1)
        while not DateUtils.is_business_day(prev_day):
            prev_day -= timedelta(days=1)
        return prev_day
    
    @staticmethod
    def add_business_days(start_date: date, business_days: int) -> date:
        """Add business days to a date, skipping weekends."""
        current_date = start_date
        days_added = 0
        
        while days_added < business_days:
            current_date += timedelta(days=1)
            if DateUtils.is_business_day(current_date):
                days_added += 1
        
        return current_date
    
    @staticmethod
    def subtract_business_days(start_date: date, business_days: int) -> date:
        """Subtract business days from a date, skipping weekends."""
        current_date = start_date
        days_subtracted = 0
        
        while days_subtracted < business_days:
            current_date -= timedelta(days=1)
            if DateUtils.is_business_day(current_date):
                days_subtracted += 1
        
        return current_date
    
    @staticmethod
    def count_business_days(start_date: date, end_date: date) -> int:
        """Count business days between two dates (inclusive)."""
        if start_date > end_date:
            return 0
        
        business_days = 0
        current_date = start_date
        
        while current_date <= end_date:
            if DateUtils.is_business_day(current_date):
                business_days += 1
            current_date += timedelta(days=1)
        
        return business_days
    
    @staticmethod
    def get_month_range(year: int, month: int) -> Tuple[date, date]:
        """Get the first and last day of a month."""
        first_day = date(year, month, 1)
        last_day = date(year, month, calendar.monthrange(year, month)[1])
        return first_day, last_day
    
    @staticmethod
    def get_quarter_range(year: int, quarter: int) -> Tuple[date, date]:
        """Get the first and last day of a quarter."""
        if quarter not in [1, 2, 3, 4]:
            raise ValueError("Quarter must be 1, 2, 3, or 4")
        
        start_month = (quarter - 1) * 3 + 1
        end_month = quarter * 3
        
        first_day = date(year, start_month, 1)
        last_day = date(year, end_month, calendar.monthrange(year, end_month)[1])
        
        return first_day, last_day
    
    @staticmethod
    def get_year_range(year: int) -> Tuple[date, date]:
        """Get the first and last day of a year."""
        first_day = date(year, 1, 1)
        last_day = date(year, 12, 31)
        return first_day, last_day
    
    @staticmethod
    def is_holiday_period(check_date: date) -> bool:
        """Check if date falls during common holiday periods."""
        month = check_date.month
        day = check_date.day
        
        # Christmas/New Year period
        if (month == 12 and day >= 20) or (month == 1 and day <= 5):
            return True
        
        # Summer vacation period (July-August)
        if month in [7, 8]:
            return True
        
        # Thanksgiving week (US - last Thursday of November)
        if month == 11:
            # Find last Thursday of November
            last_day = calendar.monthrange(check_date.year, 11)[1]
            last_thursday = None
            for day_num in range(last_day, 0, -1):
                test_date = date(check_date.year, 11, day_num)
                if test_date.weekday() == 3:  # Thursday
                    last_thursday = day_num
                    break
            
            if last_thursday and day >= last_thursday - 2:  # Week of Thanksgiving
                return True
        
        return False
    
    @staticmethod
    def get_age_in_days(start_date: date, end_date: Optional[date] = None) -> int:
        """Get age in days from start date to end date (or today)."""
        if end_date is None:
            end_date = date.today()
        return (end_date - start_date).days
    
    @staticmethod
    def get_age_in_business_days(start_date: date, end_date: Optional[date] = None) -> int:
        """Get age in business days from start date to end date (or today)."""
        if end_date is None:
            end_date = date.today()
        return DateUtils.count_business_days(start_date, end_date)
    
    @staticmethod
    def format_duration(days: int) -> str:
        """Format duration in days to human-readable string."""
        if days == 0:
            return "Today"
        elif days == 1:
            return "1 day"
        elif days < 7:
            return f"{days} days"
        elif days < 30:
            weeks = days // 7
            remaining_days = days % 7
            if weeks == 1:
                week_str = "1 week"
            else:
                week_str = f"{weeks} weeks"
            
            if remaining_days == 0:
                return week_str
            elif remaining_days == 1:
                return f"{week_str}, 1 day"
            else:
                return f"{week_str}, {remaining_days} days"
        else:
            months = days // 30
            remaining_days = days % 30
            if months == 1:
                month_str = "1 month"
            else:
                month_str = f"{months} months"
            
            if remaining_days == 0:
                return month_str
            elif remaining_days < 7:
                return f"{month_str}, {remaining_days} days"
            else:
                weeks = remaining_days // 7
                if weeks == 1:
                    return f"{month_str}, 1 week"
                else:
                    return f"{month_str}, {weeks} weeks"
    
    @staticmethod
    def get_relative_date_description(target_date: date, reference_date: Optional[date] = None) -> str:
        """Get relative description of a date (e.g., 'yesterday', 'next week')."""
        if reference_date is None:
            reference_date = date.today()
        
        diff_days = (target_date - reference_date).days
        
        if diff_days == 0:
            return "today"
        elif diff_days == 1:
            return "tomorrow"
        elif diff_days == -1:
            return "yesterday"
        elif 2 <= diff_days <= 6:
            return f"in {diff_days} days"
        elif -6 <= diff_days <= -2:
            return f"{abs(diff_days)} days ago"
        elif diff_days == 7:
            return "next week"
        elif diff_days == -7:
            return "last week"
        elif 8 <= diff_days <= 13:
            return "in about a week"
        elif -13 <= diff_days <= -8:
            return "about a week ago"
        elif 14 <= diff_days <= 30:
            weeks = diff_days // 7
            return f"in {weeks} weeks"
        elif -30 <= diff_days <= -14:
            weeks = abs(diff_days) // 7
            return f"{weeks} weeks ago"
        elif diff_days > 30:
            months = diff_days // 30
            return f"in {months} months"
        else:
            months = abs(diff_days) // 30
            return f"{months} months ago"
    
    @staticmethod
    def get_urgency_level(target_date: date, reference_date: Optional[date] = None) -> str:
        """Get urgency level based on how close the target date is."""
        if reference_date is None:
            reference_date = date.today()
        
        diff_days = (target_date - reference_date).days
        
        if diff_days < 0:
            return "overdue"
        elif diff_days == 0:
            return "due_today"
        elif diff_days <= 1:
            return "urgent"
        elif diff_days <= 3:
            return "high"
        elif diff_days <= 7:
            return "medium"
        elif diff_days <= 14:
            return "normal"
        else:
            return "low"
    
    @staticmethod
    def get_timeline_overlap(start1: date, end1: date, start2: date, end2: date) -> Optional[Tuple[date, date]]:
        """Get the overlapping period between two date ranges."""
        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)
        
        if overlap_start <= overlap_end:
            return overlap_start, overlap_end
        return None
    
    @staticmethod
    def get_available_dates(start_date: date, end_date: date, 
                          exclude_weekends: bool = True,
                          exclude_holidays: bool = True) -> List[date]:
        """Get list of available dates within a range."""
        available_dates = []
        current_date = start_date
        
        while current_date <= end_date:
            include_date = True
            
            if exclude_weekends and DateUtils.is_weekend(current_date):
                include_date = False
            
            if exclude_holidays and DateUtils.is_holiday_period(current_date):
                include_date = False
            
            if include_date:
                available_dates.append(current_date)
            
            current_date += timedelta(days=1)
        
        return available_dates


class TimeUtils:
    """Utility class for time operations."""
    
    @staticmethod
    def now_utc() -> datetime:
        """Get current UTC datetime."""
        return datetime.utcnow()
    
    @staticmethod
    def format_timestamp(dt: datetime, include_seconds: bool = True) -> str:
        """Format datetime as readable timestamp."""
        if include_seconds:
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return dt.strftime("%Y-%m-%d %H:%M")
    
    @staticmethod
    def parse_timestamp(timestamp_str: str) -> datetime:
        """Parse timestamp string to datetime."""
        # Try different formats
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse timestamp: {timestamp_str}")
    
    @staticmethod
    def get_time_ago(dt: datetime, reference_dt: Optional[datetime] = None) -> str:
        """Get human-readable time ago string."""
        if reference_dt is None:
            reference_dt = datetime.utcnow()
        
        diff = reference_dt - dt
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = int(seconds // 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
