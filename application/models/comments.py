from database import db
from application.utils.validation_mixin import ValidationMixin

class Comment(db.Model, ValidationMixin):
    __tablename__  = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    discussion_id = db.Column(db.Integer, db.ForeignKey('discussions.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    content = db.Column(db.String)
    posted_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    edited_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    discussion = db.relationship('Discussion', back_populates='comments')
    student = db.relationship('Student', back_populates='comments')
    instructor = db.relationship('Instructor', back_populates='comments')

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
        