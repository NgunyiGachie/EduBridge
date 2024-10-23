"""
This module defines the Instructor model, representing an instructor in the system,
including validation for various fields and password management.
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from sqlalchemy.orm import validates
from database import db

ph = PasswordHasher()

class Instructor(db.Model):
    """Represents an instructor with personal information, authentication,
    and relationships with other models."""

    __tablename__ = 'instructors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String)
    department = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=False)

    course = db.relationship(
        'Course', back_populates='instructor', cascade="all, delete-orphan"
    )
    lecture = db.relationship(
        'Lecture', back_populates='instructor', cascade="all, delete-orphan"
    )
    attendance = db.relationship(
        'Attendance', back_populates='instructor', cascade="all, delete-orphan"
    )
    comments = db.relationship(
        'Comment', back_populates='instructor', cascade="all, delete-orphan"
    )
    notification = db.relationship(
        'Notification', back_populates='instructor', cascade="all, delete-orphan"
    )

    @property
    def password_hash(self):
        """Prevent viewing the password hash."""
        raise AttributeError("Password hashes cannot be viewed")

    @password_hash.setter
    def password_hash(self, password):
        """Set the password hash."""
        self._password_hash = ph.hash(password)

    def authenticate(self, password):
        """Authenticate the instructor by verifying the password."""
        try:
            ph.verify(self._password_hash, password)
            return True
        except VerificationError:
            return False

    @validates('name', 'profile_picture', 'bio', 'department')
    def validate_strings(self, key, value):
        """Validate that string fields are non-empty and of type string."""
        if value is None:
            raise ValueError(f"{key} cannot be None")
        if not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        if not value.strip():
            raise ValueError(f"{key} must be a non-empty string")
        return value

    @validates('email')
    def validate_email(self, key, email):
        """Validate the email format and uniqueness."""
        if not email:
            raise AssertionError('No email provided')
        if Instructor.query.filter(Instructor.email == email).first():
            raise AssertionError("Email is already in use")
        if '@' not in email:
            raise AssertionError("Invalid email")
        return email

    def to_dict(self):
        """Return a dictionary representation of the Instructor instance."""
        return {
            'id': self.id,
            'email': self.email,
            'profile_picture': self.profile_picture,
            'department': self.department,
            'bio': self.bio
        }

    def __repr__(self):
        """Return a string representation of the model instance."""
        return f"<Instructor {self.name}, ID: {self.id}>"
