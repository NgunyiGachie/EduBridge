"""
This module defines the Attendance model and its associated validations.
"""

from datetime import datetime
from sqlalchemy.orm import validates
from database import db

class Attendance(db.Model):
    """Model for student attendance records."""

    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey("lectures.id"), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    attendance_status = db.Column(db.String, nullable=False)
    dates = db.Column(db.DateTime, nullable=False)

    student = db.relationship('Student', back_populates='attendance')
    lecture = db.relationship('Lecture', back_populates='attendance')
    instructor = db.relationship('Instructor', back_populates='attendance')

    @validates('dates')
    def validate_dates(self, value):
        """Validate that dates is a valid datetime."""
        if not isinstance(value, datetime):
            raise AttributeError("dates must be a valid datetime")
        return value

    @validates('attendance_status')
    def validate_attendance_status(self, attendance_status):
        """Validate that attendance_status is either 'present' or 'absent'."""
        if not isinstance(attendance_status, str):
            raise ValueError("Attendance status must be a string")

        attendance_status = attendance_status.strip().lower()

        if attendance_status is None:
            raise ValueError("Attendance status cannot be None")
        if attendance_status not in ['present', 'absent']:
            raise ValueError('Attendance status must be either present or absent')
        return attendance_status

    def to_dict(self):
        """Convert the Attendance instance to a dictionary."""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'lecture_id': self.lecture_id,
            'attendance_status': self.attendance_status,
            'dates': self.dates.isoformat()
        }

    def __repr__(self):
        """Return string representation of the model instance."""
        return f"<Attendance {self.id}>"
