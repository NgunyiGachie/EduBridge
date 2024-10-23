"""
This module defines the File model, which represents uploaded files and includes
validation for file metadata and upload date.
"""

from datetime import datetime
from sqlalchemy.orm import validates
from database import db

class File(db.Model):
    """Represents an uploaded file with related metadata, including information, relation, and upload date."""

    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    file_info = db.Column(db.String, nullable=False)
    related_to = db.Column(db.String, nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)

    @validates('file_info', 'related_to')
    def validate_strings(self, _, value):
        """Validate that file_info and related_to are valid strings with at least one character."""
        if value is None:
            raise ValueError("File info and related to cannot be None")
        if not isinstance(value, str):
            raise ValueError("File info and related to must be strings")
        if len(value) <= 0:
            raise ValueError("File info and related to must be at least one character")
        return value

    @validates('upload_date')
    def validate_upload_date(self, _, value):
        """Validate that upload_date is a valid datetime instance."""
        if not isinstance(value, datetime):
            raise AttributeError("Upload date must be a valid datetime")
        return value

    def to_dict(self):
        """Return the dictionary representation of the File instance."""
        return {
            'id': self.id,
            'file_info': self.file_info,
            'related_to': self.related_to,
            'upload_date': self.upload_date
        }

    def __repr__(self):
        """Return a string representation of the File instance."""
        return f"<File {self.file_info}, ID: {self.id}>"
