from database import db
from sqlalchemy.orm import validates
from datetime import datetime

class Attendance(db.Model):
    __tablename__  = 'attendances'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey("lectures.id"), nullable=False)
    attendance_status = db.Column(db.String, nullable=False)
    dates = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    student = db.relationship('Student', back_populates='attendance', lazy="dynamic", cascade="all, delete-orphan")
    lecture = db.relationship('Lecture', back_populates='attendance', lazy="dynamic", cascade="all, delete-orphan")

    @validates('dates')
    def validate_dates(self, key, value):
        if not isinstance(value, datetime):
            raise AttributeError(f"{key} must be a valid datetime")
        if value > datetime.now():
            raise ValueError(f"{key} cannot be in the future.")
        return value
    
    @validates('attendance_status')
    def validates_attendance_status(self, key, attendance_status):
        if not isinstance(attendance_status, str):
            raise ValueError("Attendance status must be a string")
        attendance_status = attendance_status.strip().lower()
        if attendance_status is None:
            return ValueError("Attendance status cannot be None")
        if attendance_status not in ['present', 'absent']:
            return ValueError('Attendance status must be either present or absent')
        return attendance_status
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'lecture_id': self.lecture_id,
            'attendance_status': self.attendance_status,
            'dates': self.dates
        }
    
    def __repr__(self):
        return f"<Attendance {self.id}>"
        
    