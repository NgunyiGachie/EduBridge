"""
This module defines the Discussion model, including relationships to Course and Comment models.
It also validates the title, description, and datetime fields.
"""

from datetime import datetime
from sqlalchemy.orm import validates
from database import db

class Discussion(db.Model):
    """Represents a discussion within a course, including title, description, and related comments."""

    __tablename__ = 'discussions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    course = db.relationship('Course', back_populates='discussion')
    comments = db.relationship('Comment', back_populates='discussion', cascade='all, delete-orphan')

    @validates('title', 'description')
    def validate_strings(self, key, value):
        """Ensure that title and description are valid, non-empty strings."""
        if value is None:
            raise ValueError(f"{key.capitalize()} cannot be None")
        if not isinstance(value, str):
            raise ValueError(f"{key.capitalize()} must be a string")
        if len(value) == 0:
            raise ValueError(f"{key.capitalize()} must contain at least one character")
        return value

    @validates('created_at', 'updated_at')
    def validate_dates(self, key, value):
        """Ensure that created_at and updated_at are valid datetime objects."""
        if not isinstance(value, datetime):
            raise AttributeError(f"{key} must be a valid datetime")
        return value

    def to_dict(self):
        """Convert the Discussion instance to a dictionary representation."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'course_id': self.course_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        """Return a string representation of the Discussion instance."""
        return f"<Discussion {self.title}, ID: {self.id}>"
