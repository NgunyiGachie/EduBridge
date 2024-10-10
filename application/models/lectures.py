from database import db
from sqlalchemy.types import JSON
from sqlalchemy.orm import validates
from datetime import datetime

class Lecture(db.Model):
    __tablename__  = 'lectures'
    id = db.Column(db.Integer, primary_key=True)
    lecture_info = db.Column(db.String, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    schedule = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    instructor = db.relationship('Instructor', back_populates='lecture')
    attendance = db.relationship('Attendance', back_populates='lecture')

    @validates('lecture_info')
    def validate_strings(self, key, value):
        if not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        if not value.strip():
            raise ValueError(f"{key} must be a non-empty string")

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
    
    @validates('created_at', 'updated_at')
    def validate_dates(self, key, value):
        if value is None:
            return None   
        if not isinstance(value, datetime):
            raise AttributeError(f"{key} must be a valid datetime")
        if value > datetime.now():
            raise ValueError(f"{key} cannot be in the future") 
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'lecture_info': self.lecture_info,
            'instructor_id': self.instructor_id,
            'schedule': self.schedule,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __repr__(self):
        """Return string representation of the model instance."""
        return f"<Lecture {self.id}>"
    