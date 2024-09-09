from database import db
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt

bcrypt= Bcrypt()

class Instructors(db.Model):
    __table__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String)

    ##relationships
    

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes cannot be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password.encode("utf-8"))

    
