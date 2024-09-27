from database import db
from sqlalchemy.types import JSON
from application.utils.validation_mixin import ValidationMixin

class Lecture(db.Model, ValidationMixin):
    __tablename__  = 'lectures'
    id = db.Column(db.Integer, primary_key=True)
    lecture_info = db.Column(db.String, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    schedule = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    instructor = db.relationship('Instructor', back_populates='lecture')
    attendance = db.relationship('Attendance', back_populates='lecture')

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
    