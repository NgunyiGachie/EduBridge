from database import db
from application.utils.validation_mixin import ValidationMixin

class Discussion(db.Model, ValidationMixin):
    __tablename__   = 'discussions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    course = db.relationship('Course', back_populates='discussion')
    comments = db.relationship('Comment', back_populates='discussion', cascade='all, delete-orphan')

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
        
    
