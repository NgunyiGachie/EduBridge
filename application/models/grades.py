from database import db
from application.utils.validation_mixin import ValidationMixin

class Grade(db.Model, ValidationMixin):
    __tablename__  = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    student = db.relationship('Student', back_populates='grade')
    course = db.relationship('Course', back_populates='grade')
    submission = db.relationship('Submission', back_populates='grade', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'student_id': self.student_id,
            'grade': self.grade,
            'date_posted': self.date_posted
        }
    
    def __repr__(self):
        return f"<Grade {self.id}>"