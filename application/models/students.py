"""
This module defines the Student model, representing a student in the
system with fields for personal information, password hashing, and
validation methods.
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from sqlalchemy.orm import validates
from database import db

ph = PasswordHasher()

class Student(db.Model):
    """Represents a student, including personal details, password
    management, and relationships with other models."""

    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String, nullable=False)

    submission = db.relationship('Submission', back_populates='student',
                                cascade="all, delete-orphan")
    enrollment = db.relationship('Enrollment', back_populates='student',
                                cascade="all, delete-orphan")
    grade = db.relationship('Grade', back_populates='student',
                            cascade="all, delete-orphan")
    attendance = db.relationship('Attendance', back_populates='student',
                                cascade="all, delete-orphan")
    comments = db.relationship('Comment', back_populates='student',
                            cascade="all, delete-orphan")
    notification = db.relationship('Notification', back_populates='student',
                                cascade="all, delete-orphan")

    @property
    def password_hash(self):
        """Prevent access to the password hash."""
        raise AttributeError("Password hashes cannot be viewed")

    @password_hash.setter
    def password_hash(self, password):
        """Set the password hash after hashing the provided password."""
        self._password_hash = ph.hash(password)

    def authenticate(self, password):
        """Verify the provided password against the stored password hash."""
        try:
            ph.verify(self._password_hash, password)
            return True
        except VerificationError:
            return False

    @validates('first_name', 'last_name', 'profile_picture')
    def validate_strings(self, key, value):
        """Validate that the provided strings are non-empty."""
        if value is None:
            raise ValueError(f"{key} cannot be None")
        if not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        if not value.strip():
            raise ValueError(f"{key} must be a non-empty string")
        return value

    @validates("username")
    def validate_username(self, username):
        """Validate the username for uniqueness and length constraints."""
        if not username:
            raise AssertionError("No username provided")
        if Student.query.filter(Student.username == username).first():
            raise AssertionError("Username is already in use")
        if len(username) < 5 or len(username) > 20:
            raise AssertionError('Username must be between 5 and 20 characters')
        return username

    @validates('email')
    def validate_email(self, email):
        """Validate the email for uniqueness and format constraints."""
        if not email:
            raise AssertionError('No email provided')
        if Student.query.filter(Student.email == email).first():
            raise AssertionError("Email is already in use")
        if '@' not in email:
            raise AssertionError("Invalid email")
        return email

    def to_dict(self):
        """Return a dictionary representation of the Student instance."""
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
