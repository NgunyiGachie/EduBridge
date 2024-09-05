from database import db

class Users(db.Model):
    __table__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String)