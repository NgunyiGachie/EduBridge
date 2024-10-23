"""
This module defines the Lecture model, representing a lecture in the system,
including validation for various fields and relationships with other models.
"""

from datetime import datetime
from sqlalchemy.types import JSON
from sqlalchemy.orm import validates
from database import db

class Lecture(db.Model):
    """Represents a lecture with information about the lecture,
    its instructor, schedule, and timestamps for creation and updates."""

    __tablename__ = 'lectures'

    id = db.Column(db.Integer, primary_key=True)
    lecture_info = db.Column(db.String, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    schedule = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    instructor = db.relationship('Instructor', back_populates='lecture')
    attendance = db.relationship('Attendance', back_populates='lecture')

    @validates('lecture_info')
    def validate_strings(self, key, value):
        """Validate that the lecture_info is a non-empty string."""
        if not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        if not value.strip():
            raise ValueError(f"{key} must be a non-empty string")
        return value

    @validates('schedule')
    def validate_schedule(self, key, schedule):
        """Validate that the schedule is a list of dictionaries
        containing 'day', 'start', and 'end' keys."""
        if not isinstance(schedule, list):
            raise ValueError(f"{key} must be a list of entries")
        for entry in schedule:
            if not isinstance(entry, dict):
                raise ValueError(f"Each entry in {key} must be a dictionary")
            if not all(k in entry for k in ['day', 'start', 'end']):
                raise ValueError(f"Each entry in {key} must contain 'day', 'start', and 'end'")
        return schedule

    @validates('created_at', 'updated_at')
    def validate_dates(self, key, value):
        """Validate that date fields are valid datetime objects
        and not set in the future."""
        if value is None:
            return None
        if not isinstance(value, datetime):
            raise TypeError(f"{key} must be a valid datetime")
        if value > datetime.now():
            raise ValueError(f"{key} cannot be in the future")
        return value

    def to_dict(self):
        """Return a dictionary representation of the Lecture instance."""
        return {
            'id': self.id,
            'lecture_info': self.lecture_info,
            'instructor_id': self.instructor_id,
            'schedule': self.schedule,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        """Return a string representation of the model instance."""
        return f"<Lecture {self.id}>"
