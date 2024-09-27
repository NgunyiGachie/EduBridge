from database import db
from application.utils.validation_mixin import ValidationMixin

class Notification(db.Model, ValidationMixin):
    __tablename__  = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    message_body = db.Column(db.String, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    read_status = db.Column(db.String, nullable=False)
    sent_date = db.Column(db.DateTime, server_default= db.func.now(), nullable=False)
    read_date = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    student = db.relationship('Student', back_populates='notification')
    instructor = db.relationship('Instructor', back_populates='notification')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message_body': self.message_body,
            'student_id': self.student_id,
            'instructor_id': self.instructor_id,
            'read_status': self.read_status,
            'sent_date': self.sent_date,
            'read_date': self.read_date
        }
    
    def __repr__(self):
        return f"<Notification {self.id}>"
    