from database import db
from sqlalchemy.orm import validates
from sqlalchemy.types import JSON
from datetime import datetime

class Lecture(db.Model):
    __tablename__  = 'lectures'
    id = db.Column(db.Integer, primary_key=True)
    lecture_info = db.Column(db.String, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    schedule = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    instructor = db.relationship('Instructor', back_populates='lecture', lazy='dynamic', cascade='all, delete-orphan')

    @validates('lecture_info')
    def validate_lecture_info(self, key, value):
        if value is None:
            raise AssertionError('Lecture info cannot be None')
        if not isinstance(value, str):
            raise AssertionError('Lecture info must be of type string')
        if len(value) <= 0:
            raise AssertionError("Lecture info must be at least one character")
        return value
    
    @validates('schedule')
    def validate_schedule(self, key, schedule):
        if not isinstance(schedule, list):
            raise ValueError("Schedule must be a list of entries")
        for entry in schedule:
            if not isinstance(entry, dict):
                raise ValueError("Each entry must be of type dictionary")
            if 'day' not in entry or 'start_time' not in entry or 'end_time' not in entry:
                raise ValueError("Each entry must contain the day, start time, and end time")
        return schedule

    @validates('created_at', 'updated_at')
    def validate_dates(self, key, value):
        if not isinstance(value, datetime):
            raise AttributeError(f"{key} must be a valid datetime")
        if value > datetime.now():
            raise ValueError(f"{key} cannot be in the future.")
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
        return f"<Lecture {self.id}>"
    