from database import db
from sqlalchemy.orm import validates
from datetime import datetime

class Comment(db.Model):
    __tablename__  = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    discussion_id = db.Column(db.Integer, db.ForeignKey('discussions.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    content = db.Column(db.String, nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False)
    edited_at = db.Column(db.DateTime, nullable=False)

    discussion = db.relationship('Discussion', back_populates='comments')
    student = db.relationship('Student', back_populates='comments')
    instructor = db.relationship('Instructor', back_populates='comments')

    @validates('content')
    def validate_content(self, key, content):
        if content is None:
            raise AssertionError("Content cannot be None")
        if len(content) <= 0:
            raise AssertionError("Content must be above 0 characters")
        if not content or not (content, str):
            raise AssertionError("Content must be of type string")
        return content
    
    @validates('posted_at', 'edited_at')
    def validate_dates(self, key, value):
        if not isinstance(value, datetime):
            raise AttributeError(f"{key} must be a valid datetime")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'instructor_id': self.instructor_id,
            'content': self.content,
            'posted_at': self.posted_at,
            'edited_at': self.edited_at
        }
    
    def __repr__(self):
        """Return string representation of the model instance."""
        return f"<Comment {self.id}>"
        