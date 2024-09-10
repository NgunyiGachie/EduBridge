from database import db
from sqlalchemy.orm import validates
from datetime import datetime

class Assignment(db.Model):
    __table__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    due_date = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    total_points = db.Column(db.Integer, nullable=False)

    course = db.relationship('Course', back_populates='assignment', lazy="dynamic", cascade="all, delete-orphan")
    submission = db.relationship('Submission', back_populates='assignment', lazy="dynamic", cascade="all, delete-orphan")

    @validates('title', 'description')
    def validate_strings(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        if not value.strip():
            raise ValueError(f'{key} must be a non-empty string')
        return value
    
    @validates('due_date')
    def validate_due_date(self, key, value):
        if not isinstance(value, datetime):
            raise AttributeError(f"{key} must be a valid datetime")
        return value
    
    @validates('total_points')
    def validate_total_points(self, key, total_points):
        if total_points is None:
            raise ValueError("Total points cannot be None")
        if not isinstance(total_points, int):
            raise ValueError("Total points must be an integer")
        if total_points < 0:
            raise ValueError("Total points must be greater than or equal to zero")
        return total_points
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'course_id': self.course_id,
            'due_date': self.due_date,
            'total_points': self.total_points
        }
    
    def __repr__(self):
        return f"<Assignment {self.title}, ID: {self.id}>"
        
