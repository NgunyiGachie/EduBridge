from database import db
from sqlalchemy.orm import validates
from datetime import datetime

class Notification(db.Model):
    __table__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    message_body = db.Column(db.String, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id', nullable=False))
    read_status = db.Column(db.String, nullable=False)
    sent_date = db.Column(db.DateTime, server_default= db.func.now(), nullable=False)
    read_date = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    student = db.relationship('Student', back_populates='notification', lazy='dynamic', cascade='all, delete-orphan')
    instructor = db.relationship('Instructor', back_populates='notification', lazy='dynamic', cascade='all, delete-orphan')

    @validates('title', 'message_body')
    def validate_strings(self, key, value):
        if value is None:
            raise AssertionError("Title and message body cannot be None")
        if not isinstance(value, str):
            raise AssertionError("Title and message body must be of type string")
        if len(value) <= 0:
            raise AssertionError("Title and message body must be at least one character")
        return value
    
    @validates('read_status')
    def validate_read_status(self, key, value):
        if value is None:
            raise AssertionError("Read status cannot be None")
        if not isinstance(value, str):
            raise AssertionError("Read status must be of type string")
        if value not in ["read", 'unread']:
            raise AssertionError("Read status must be either read or unread")
        return value
    
    @validates('sent_date', 'read_date')
    def validate_dates(self, key, value):
        if not isinstance(value, datetime):
            raise AttributeError(f"{key} must be a valid datetime")
        return value
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message_body': self.message_body,
            'student_id': self.student_id,
            'instructor_id': self.instructor_id,
            'read_status': self.read_status,
            'sent_date': self.sent_date,
            'read_date': self.read_date
        }
    
    def __repr__(self):
        return f"<Notification {self.id}>"
    