from database import db
from application.utils.validation_mixin import ValidationMixin

class Attendance(db.Model, ValidationMixin):
    __tablename__  = 'attendances'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey("lectures.id"), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False) 
    attendance_status = db.Column(db.String, nullable=False)
    dates = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    student = db.relationship('Student', back_populates='attendance')
    lecture = db.relationship('Lecture', back_populates='attendance')
    instructor = db.relationship('Instructor', back_populates='attendance') 
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'lecture_id': self.lecture_id,
            'attendance_status': self.attendance_status,
            'dates': self.dates
        }
    
    def __repr__(self):
        """Return string representation of the model instance."""
        return f"<Attendance {self.id}>"
        
    