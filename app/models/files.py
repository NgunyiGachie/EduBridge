from database import db
from sqlalchemy.orm import validates
from datetime import datetime

class File(db.Model):
    __table__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    file_info = db.Column(db.String, nullable=False)
    related_to = db.Column(db.String, nullable=False)
    upload_date = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    @validates('file_info', 'related_to')
    def validate_strings(self, key, value):
        if value is None:
            raise ValueError("File info and related to cannot be None")
        if not isinstance(value, str):
            raise ValueError("File info and related to must be of type string")
        if len(value) <= 0:
            raise ValueError("File info and related to must be at least one character")
        return value
    
    @validates('upload_date')
    def validate_upload_date(self, key, value):
        if not isinstance(value, datetime):
            raise AttributeError(f"{key} must be a valid datetime")
        return value
    
    def to_dict(self):
        return {
            'id': self.id,
            'file_info': self.file_info,
            'related_to': self.related_to,
            'upload_date': self.upload_date
        }
    
    def __repr__(self):
        return f"<File {self.file_info}, ID: {self.id}>"
        