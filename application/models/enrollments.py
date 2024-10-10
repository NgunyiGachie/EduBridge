from database import db
from sqlalchemy.orm import validates

class Enrollment(db.Model):
    __tablename__  = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    status = db.Column(db.String, nullable=False)

    course = db.relationship('Course', back_populates='enrollment')
    student = db.relationship('Student', back_populates='enrollment')

    @validates('status')
    def validate_status(self, key, status):
        if status is None:
            raise AssertionError("Status cannot be None")
        if not isinstance(status, str):
            raise ValueError("Status must be of type string")
        if status not in ['enrolled', 'pending', 'dropped']:
            raise AssertionError("Status has to be enrolled, pending, or enrolled")
        return status
   
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'student_id': self.student_id,
            'status': self.status
        }
       
    def __repr__(self):
        """Return string representation of the model instance."""
        return f"<Enrollment {self.id}>"