from database import db
from application.utils.validation_mixin import ValidationMixin

class Submission(db.Model, ValidationMixin):
    __tablename__  = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    submission_info = db.Column(db.String, nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'), nullable=False)
    date = db.Column(db.DateTime, server_default = db.func.now(), nullable=False)

    assignment = db.relationship('Assignment', back_populates='submission')
    student = db.relationship('Student', back_populates='submission')
    grade = db.relationship('Grade', back_populates='submission')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'assignment_id': self.assignment_id,
            'grade_id': self.grade_id,
            'submission_info': self.submission_info,
            'date': self.date
        }
    
    def __repr__(self):
        return f"<Submission {self.id}>"