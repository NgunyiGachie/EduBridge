from database import db
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from sqlalchemy.orm import validates
from application.utils.validation_mixin import ValidationMixin

ph = PasswordHasher()

class Instructor(db.Model, ValidationMixin):
    __tablename__  = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email= db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String)
    department = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)

    course = db.relationship('Course', back_populates='instructor', cascade="all, delete-orphan")
    lecture = db.relationship('Lecture', back_populates='instructor', cascade="all, delete-orphan")
    attendance = db.relationship('Attendance', back_populates='instructor', cascade="all, delete-orphan")
    comments = db.relationship('Comment', back_populates='instructor', cascade="all, delete-orphan")
    notification = db.relationship('Notification', back_populates='instructor', cascade="all, delete-orphan")

    @property
    def password_hash(self):
        raise AttributeError("Password hashes cannot be viewed")
    
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = ph.hash(password)

    def authenticate(self, password):
        try:
            ph.verify(self._password_hash, password)
            return True
        except VerificationError:
            return False
        
    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')
        if Instructor.query.filter(Instructor.email == email).first():
            raise AssertionError("Email is already in use")
        if '@' not in email:
            raise AssertionError("Invalid email")
        return email
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'profile_picture': self.profile_picture,
            'department': self.department,
            'bio': self.bio
        }
    
    def __repr__(self):
        return f"<Instructor {self.name}, ID: {self.id}>"
        

    
