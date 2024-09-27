from database import db
from sqlalchemy.types import JSON
from application.utils.validation_mixin import ValidationMixin

class Course(db.Model, ValidationMixin):
    __tablename__  = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_info = db.Column(db.String, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    schedule = db.Column(JSON, nullable=False)

    instructor = db.relationship('Instructor', back_populates='course')
    discussion = db.relationship('Discussion', back_populates='course', cascade='all, delete-orphan')
    enrollment = db.relationship('Enrollment', back_populates='course', cascade='all, delete-orphan')
    grade = db.relationship('Grade', back_populates='course', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'course_info': self.course_info,
            'instructor_id': self.instructor_id,
            'schedule': self.schedule
        }
    
    def __repr__(self):
        return f"<Course {self.course_info}, ID: {self.id}>"
        