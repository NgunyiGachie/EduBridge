"""
This module defines the Grade model, which represents the grades assigned to students
for a specific course, including validation for grades and date posted.
"""

from datetime import datetime
from sqlalchemy.orm import validates
from database import db

class Grade(db.Model):
    """Represents a student's grade for a course, including the student and course relationships."""

    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)

    student = db.relationship('Student', back_populates='grade')
    course = db.relationship('Course', back_populates='grade')
    submission = db.relationship('Submission', back_populates='grade', cascade='all, delete-orphan')

    @validates('grade')
    def validate_grade(self, _, grade):
        """Validate that the grade is an integer between 1 and 100."""
        if grade is None:
            raise AssertionError('Grades cannot be None')
        if not isinstance(grade, int):
            raise AssertionError("Grades must be an integer")
        if grade < 1 or grade > 100:
            raise ValueError("Grades must be between 1 and 100")
        return grade

    @validates('date_posted')
    def validate_dates(self, _, value):
        """Validate that date_posted is a valid datetime object."""
        if not isinstance(value, datetime):
            raise AttributeError(f"{value} must be a valid datetime")
        return value

    def to_dict(self):
        """Return a dictionary representation of the Grade instance."""
        return {
            'id': self.id,
            'course_id': self.course_id,
            'student_id': self.student_id,
            'grade': self.grade,
            'date_posted': self.date_posted
        }

    def __repr__(self):
        """Return a string representation of the Grade instance."""
        return f"<Grade {self.id}>"
