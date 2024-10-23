"""
This module defines the Enrollment model, representing the association between students and courses.
It includes relationships to the Course and Student models, and validates the status field.
"""

from sqlalchemy.orm import validates
from database import db

class Enrollment(db.Model):
    """
    Represents a student's enrollment in a course.
    It includes statuses of 'enrolled', 'pending', or 'dropped'.
    """

    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    status = db.Column(db.String, nullable=False)

    course = db.relationship('Course', back_populates='enrollment')
    student = db.relationship('Student', back_populates='enrollment')

    @validates('status')
    def validate_status(self, _, status):
        """Ensure the status is one of 'enrolled', 'pending', or 'dropped'."""
        if status is None:
            raise AssertionError("Status cannot be None")
        if not isinstance(status, str):
            raise ValueError("Status must be a string")
        if status not in ['enrolled', 'pending', 'dropped']:
            raise AssertionError("Status must be 'enrolled', 'pending', or 'dropped'")
        return status

    def to_dict(self):
        """Convert the Enrollment instance to a dictionary representation."""
        return {
            'id': self.id,
            'course_id': self.course_id,
            'student_id': self.student_id,
            'status': self.status
        }

    def __repr__(self):
        """Return a string representation of the Enrollment instance."""
        return f"<Enrollment {self.id}>"
