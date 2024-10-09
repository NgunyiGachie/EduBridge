from database import db
from sqlalchemy.orm import validates
from datetime import datetime

class Submission(db.Model):
    __tablename__  = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    submission_info = db.Column(db.String, nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)


    assignment = db.relationship('Assignment', back_populates='submission')
    student = db.relationship('Student', back_populates='submission')
    grade = db.relationship('Grade', back_populates='submission')

    @validates('submission_info')
    def validate_submission_info(self, key, value):
        if not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        return value
    
    @validates('assignment_id', 'student_id', 'grade_id')
    def validate_integers(self, key, value):
        if not isinstance(value, int):
            raise ValueError(f"{key} must be an integer")
        return value

    @validates('date')
    def validate_date(self, key, value):
        print(f"Validating date: {value}") 
        if value > datetime.now():
            raise ValueError(f"{key} cannot be in the future")
        return value

    
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
        """Return string representation of the model instance."""
        return f"<Submission {self.id}>"