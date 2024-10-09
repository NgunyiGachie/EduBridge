from database import db
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from sqlalchemy.orm import validates
from application.utils.validation_mixin import ValidationMixin

ph = PasswordHasher()

class Student(db.Model, ValidationMixin):
    __tablename__  = 'students'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email= db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String)

    submission = db.relationship('Submission', back_populates='student', cascade="all, delete-orphan")
    enrollment = db.relationship('Enrollment', back_populates='student', cascade="all, delete-orphan")
    grade = db.relationship('Grade', back_populates='student', cascade="all, delete-orphan")
    attendance = db.relationship('Attendance', back_populates='student', cascade="all, delete-orphan")
    comments = db.relationship('Comment', back_populates='student', cascade="all, delete-orphan")
    notification = db.relationship('Notification', back_populates='student', cascade="all, delete-orphan")

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
        
    @validates("username")
    def validate_username(self, key, username):
        if not username:
            raise AssertionError("No username provided")
        if Student.query.filter(Student.username == username).first():
            raise AssertionError("Username is already in use")
        if len(username) < 5 or len(username) > 20:
            raise AssertionError('Username must be between 5 and 20 characters')
        return username
    
    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')
        if Student.query.filter(Student.email == email).first():
            raise AssertionError("Email is already in use")
        if '@' not in email:
            raise AssertionError("Invalid email")
        return email
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'profile_picture': self.profile_picture
        }
    
    def __repr__(self):
        """Return string representation of the model instance."""
        return f"<Student {self.username}, ID: {self.id}>"
        

    
