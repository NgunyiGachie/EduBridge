"""
This module defines the Assignment model and its associated validations.
"""

from database import db
from sqlalchemy.orm import validates
from datetime import datetime


class Assignment(db.Model):
    """Model representing an assignment."""

    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)  
    description = db.Column(db.String(1000), nullable=False) 
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    total_points = db.Column(db.Integer, nullable=False)

    course = db.relationship('Course', single_parent=True)
    submission = db.relationship('Submission', back_populates='assignment', cascade="all, delete-orphan")

    @validates('title', 'description')
    def validate_strings(self, key: str, value: str) -> str:
        """Validate that title and description are non-empty strings."""
        if not value or not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        if not value.strip():
            raise ValueError(f'{key} must be a non-empty string')
        return value
    
    @validates('due_date')
    def validate_due_date(self, key: str, value: datetime) -> datetime:
        """Validate that due_date is a valid datetime."""
        if not isinstance(value, datetime):
            raise ValueError(f"{key} must be a valid datetime")
        return value
    
    @validates('total_points')
    def validate_total_points(self, key: str, total_points: int) -> int:
        """Validate that total_points is a non-negative integer."""
        if total_points is None:
            raise ValueError("Total points cannot be None")
        if not isinstance(total_points, int):
            raise ValueError("Total points must be an integer")
        if total_points < 0:
            raise ValueError("Total points must be greater than or equal to zero")
        return total_points
    
    def to_dict(self) -> dict:
        """Convert the Assignment instance to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'course_id': self.course_id,
            'due_date': self.due_date.isoformat() if self.due_date else None,  
            'total_points': self.total_points
        }
    
    def __repr__(self) -> str:
        """Return string representation of the model instance."""
        return f"<Assignment {self.title}, ID: {self.id}>"
