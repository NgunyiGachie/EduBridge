from database import db
from application.utils.validation_mixin import ValidationMixin

class Assignment(db.Model, ValidationMixin):
    __tablename__  = 'assignments'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    due_date = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    total_points = db.Column(db.Integer, nullable=False)

    course = db.relationship('Course', single_parent=True)
    submission = db.relationship('Submission', back_populates='assignment', cascade="all, delete-orphan")

    
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
        
