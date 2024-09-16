from database import db
from sqlalchemy.orm import validates
from sqlalchemy import Json

class Course(db.Model):
    __table__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_info = db.Column(db.String, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)
    schedule = db.Column(Json, nullable=False)

    instructor = db.relationship('Instructor', back_populates='course', lazy="dynamic", cascade="all, delete-orphan")
    discussion = db.relationsip('Discussion', back_populates='course', lazy='dyamic', cascade='all, delete-orphan')

    @validates('course_info')
    def validate_course_info(self, key, value):
        if value is None:
            raise AssertionError("Course info cannot be None")
        if len(value) <= 0:
            raise AssertionError("Course info must be at least one character")
        if not value or not (value, str):
            raise ValueError("Course info must be of type string")
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
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_info': self.course_info,
            'instructor_id': self.instructor_id,
            'schedule': self.schedule
        }
    
    def __repr__(self):
        return f"<Course {self.course_info}, ID: {self.id}>"
        