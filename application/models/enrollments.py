from database import db
from application.utils.validation_mixin import ValidationMixin

class Enrollment(db.Model, ValidationMixin):
    __tablename__  = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    status = db.Column(db.String, nullable=False)

    course = db.relationship('Course', back_populates='enrollment')
    student = db.relationship('Student', back_populates='enrollment')
   
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'student_id': self.student_id,
            'status': self.status
        }
       
    def __repr__(self):
        return f"<Enrollment {self.id}>"