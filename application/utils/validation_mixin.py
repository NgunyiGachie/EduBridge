from sqlalchemy.orm import validates
from datetime import datetime
import re

class ValidationMixin:

    @validates('title', 'description', 'course_info', 'content', 'file_info', 'related_to', 'department', 'lecture_info', 
               'message_body', 'submission_info', 'name')  
    def validate_strings(self, key, value):
        if value is None:
            raise ValueError(f"{key} cannot be None")
        if not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        if not value.strip():
            raise ValueError(f"{key} must be a non-empty string")

        # Additional validation for 'name' field
        if key == 'name':
            if len(value) < 5 or len(value) > 20:
                raise ValueError('Username must be between 5 and 20 characters')

        return value

    @validates('due_date', 'posted_at', 'edited_at', 'created_at', 'date', 'updated_at', 'upload_date', 'date_posted', 'sent_date', 'read_date', 'dates')
    def validate_dates(self, key, value):
        if value is None:
            return None  
        
        if not isinstance(value, datetime):
            raise AttributeError(f"{key} must be a valid datetime")
        
        if value > datetime.now():
            raise ValueError(f"{key} cannot be in the future")
        
        return value

    @validates('total_points')
    def validate_total_points(self, key, value):
        if value is None:
            raise ValueError(f"{key} cannot be None")
        if not isinstance(value, int):
            raise ValueError(f"{key} must be an integer")
        if value < 0:
            raise ValueError(f"{key} must be greater than or equal to zero")
        return value

    @validates('attendance_status')
    def validate_attendance_status(self, key, value):
        if not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        value = value.strip().lower()
        if value not in ['present', 'absent']:
            raise ValueError(f"{key} must be either 'present' or 'absent'")
        return value

    @validates('schedule')
    def validate_schedule(self, key, schedule):
        if not isinstance(schedule, list):
            raise ValueError(f"{key} must be a list of entries")
        for entry in schedule:
            if not isinstance(entry, dict):
                raise ValueError(f"Each entry in {key} must be a dictionary")
            if not all(k in entry for k in ['day', 'start', 'end']):
                raise ValueError(f"Each entry in {key} must contain 'day', 'start', and 'end'")
        return schedule

    @validates('status')
    def validate_status(self, key, status):
        if status is None:
            raise AssertionError("Status cannot be None")
        if not isinstance(status, str):
            raise ValueError("Status must be of type string")
        if status not in ['enrolled', 'pending', 'dropped']:
            raise AssertionError("Status must be 'enrolled', 'pending', or 'dropped'")
        return status
    
    @validates('grade')
    def validate_grade(self, key, grade):
        if grade is None:
            raise AssertionError('Grades cannot be None')
        if not isinstance(grade, int):
            raise AssertionError("Grades must be an integer")
        if grade < 1 or grade > 100:
            raise ValueError("Grades must be between 1 and 100")
        return grade
    
    @validates('profile_picture')
    def validate_profile_picture(self, key, profile_picture):
        if not re.match(r'^https?://', profile_picture):
            raise AttributeError(f'{key} must be a valid URL')
        return profile_picture
    
    @validates('read_status')
    def validate_read_status(self, key, value):
        if value is None:
            raise AssertionError("Read status cannot be None")
        if not isinstance(value, str):
            raise AssertionError("Read status must be of type string")
        if value not in ["read", 'unread']:
            raise AssertionError("Read status must be either 'read' or 'unread'")
        return value
