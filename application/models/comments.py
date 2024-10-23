"""
This module defines the Comment model and its associated validations.
"""

from datetime import datetime
from sqlalchemy.orm import validates
from database import db

class Comment(db.Model):
    """Model for comments on discussions."""

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    discussion_id = db.Column(db.Integer, db.ForeignKey('discussions.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    content = db.Column(db.String, nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False)
    edited_at = db.Column(db.DateTime, nullable=False)

    discussion = db.relationship('Discussion', back_populates='comments')
    student = db.relationship('Student', back_populates='comments')
    instructor = db.relationship('Instructor', back_populates='comments')

    @validates('content')
    def validate_content(self, content):
        """Validate that the content is a non-empty string."""
        if content is None:
            raise AssertionError("Content cannot be None")
        if not isinstance(content, str) or len(content) <= 0:
            raise AssertionError("Content must be a non-empty string")
        return content

    @validates('posted_at', 'edited_at')
    def validate_dates(self, value):
        """Validate that posted_at and edited_at are valid datetime instances."""
        if not isinstance(value, datetime):
            raise AttributeError("Must be a valid datetime")
        return value

    def to_dict(self):
        """Convert the Comment instance to a dictionary."""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'instructor_id': self.instructor_id,
            'content': self.content,
            'posted_at': self.posted_at.isoformat(),
            'edited_at': self.edited_at.isoformat()
        }

    def __repr__(self):
        """Return string representation of the model instance."""
        return f"<Comment {self.id}>"
