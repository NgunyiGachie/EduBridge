from database import db
from sqlalchemy.ext.hybrid import hybrid_property
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from sqlalchemy.orm import validates
import re

ph = PasswordHasher()

class Instructor(db.Model):
    __table__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email= db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String)
    department = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)

    course = db.relationship('Course', back_populates='instructor', lazy="dynamic", cascade="all, delete-orphan")
    lecture = db.relationship('Lecture', back_populates='instructor', lazy="dynamic", cascade="all, delete-orphan")
    attendance = db.relationship('Attendance', back_populates='instructor', lazy="dynamic", cascade="all, delete-orphan")
    comment = db.relationship('Comment', back_populates='instructor', lazy="dynamic", cascade="all, delete-orphan")
    notification = db.relationship('Notification', back_populates='instructor', lazy="dynamic", cascade="all, delete-orphan")

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
        
    @validates("name")
    def validate_username(self, key, name):
        if not name:
            raise AssertionError("No username provided")
        if len(name) < 5 or len(name) > 20:
            raise AssertionError('Username must be between 5 and 20 characters')
        return name
    
    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')
        if Instructor.query.filter(Instructor.email == email).first():
            raise AssertionError("Email is already in use")
        if '@' not in email:
            raise AssertionError("Invalid email")
        return email
    
    @validates('profile_picture')
    def validate_profile_picture(self, key, profile_picture):
        if not re.match(r'^https?://', profile_picture):
            raise AttributeError(f'{key} must be a valid URL')
        return profile_picture
    
    @validates('department')
    def validate_department(self, department):
        if not isinstance(department, str):
            raise ValueError("Department must be a string")
        if not department.strip():
            raise ValueError('Department must be a non-empty string')
        return department
    
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
        

    
