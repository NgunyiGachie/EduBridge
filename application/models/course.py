"""
This module defines the Course model, including course details, schedules, and relationships
to other models such as Instructor, Discussion, Enrollment, and Grade.
"""

from sqlalchemy.types import JSON
from sqlalchemy.orm import validates
from database import db

class Course(db.Model):
    """Model for courses, including course details and schedule information."""

    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    course_info = db.Column(db.String, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    schedule = db.Column(JSON, nullable=False)

    instructor = db.relationship('Instructor', back_populates='course')
    discussion = db.relationship('Discussion', back_populates='course',
                                 cascade='all, delete-orphan')
    enrollment = db.relationship('Enrollment', back_populates='course',
                                 cascade='all, delete-orphan')
    grade = db.relationship('Grade', back_populates='course',
                            cascade='all, delete-orphan')

    @validates('course_info')
    def validate_course_info(self, value):
        """Validate that course_info is a non-empty string."""
        if value is None:
            raise AssertionError("Course info cannot be None")
        if not isinstance(value, str) or len(value) <= 0:
            raise ValueError("Course info must be a non-empty string")
        return value

    @validates('schedule')
    def validate_schedule(self, schedule):
        """Validate that schedule is a list of valid schedule entries."""
        if not isinstance(schedule, list):
            raise ValueError("Schedule must be a list of entries")
        for entry in schedule:
            if not isinstance(entry, dict):
                raise ValueError("Each entry must be of type dictionary")
            if 'day' not in entry or 'start' not in entry or 'end' not in entry:
                raise ValueError("Each entry must contain the day, start time, and end time")
        return schedule

    def to_dict(self):
        """Convert the Course instance to a dictionary."""
        return {
            'id': self.id,
            'course_info': self.course_info,
            'instructor_id': self.instructor_id,
            'schedule': self.schedule
        }

    def __repr__(self):
        """Return string representation of the model instance."""
        return f"<Course {self.course_info}, ID: {self.id}>"
