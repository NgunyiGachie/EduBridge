from database import db
from application.utils.validation_mixin import ValidationMixin

class File(db.Model, ValidationMixin):
    __tablename__  = 'files'
    id = db.Column(db.Integer, primary_key=True)
    file_info = db.Column(db.String, nullable=False)
    related_to = db.Column(db.String, nullable=False)
    upload_date = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'file_info': self.file_info,
            'related_to': self.related_to,
            'upload_date': self.upload_date
        }
    
    def __repr__(self):
        """Return string representation of the model instance."""
        return f"<File {self.file_info}, ID: {self.id}>"
        