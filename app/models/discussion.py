from database import db
from sqlalchemy.orm import validates
from datetime import datetime

class Discussion(db.Model):
    __table__ = 'discussions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    course = db.relationship('Course', back_populates='discussion', lazy='dynamic', cascade='all, delete-orphan')

    @validates('title', 'description')
    def validate_strings(self, key, value):
        if value is None:
            raise ValueError("Title and description cannot be None")
        if not isinstance(value, str):
            raise ValueError("Title and description must be of type string")
        if len(value) <= 0:
            raise ValueError("Title and description must be at least one character")
        return value
    
    @validates('created_at', 'updated_at')
    def validate_dates(self, key, value):
        if not isinstance(value, datetime):
            raise AttributeError(f"{key} must be a valid datetime")
        return value
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'course_id': self.course_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __repr__(self):
        return f"<Discussion {self.title}, ID: {self.id}>"
        
    
