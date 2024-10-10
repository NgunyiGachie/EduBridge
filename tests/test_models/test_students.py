import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.students import Student
from argon2 import PasswordHasher

ph = PasswordHasher()

class TestStudents:
    """Test case for student model"""
    def test_has_attributes(self):
        """has attributes: username, first_name, last_name, email, password_hash, profile_picture"""

        with app.app_context():
            Student.query.delete()
            db.session.commit()

            student = Student(
                username='antogachie', 
                first_name='Anthony', 
                last_name='Gachie', 
                email='myemail@gmail.com', 
                profile_picture='https://example.com/images/antogachie.jpg'
                )
            student.password_hash = ph.hash("whosafraidofvirginiawoolf")
            db.session.add(student)
            db.session.commit()

            created_student = Student.query,filter(Student.username == "antogachie").first()
            assert created_student.username == "antogachie"
            assert created_student.first_name == "Anthony"
            assert created_student.last_name == "Gachie"
            assert created_student.email == "myemail@gmail.com"
            assert created_student.profile_picture == "https://example.com/images/antogachie.jpg"
            assert created_student.password_hash is not None

    def test_requires_username(self):
        """Requires each record to have a username"""

        with app.app_context():
            Student.query.delete()
            db.session.commit()

            student = Student(
                first_name='Anthony', 
                last_name='Gachie', 
                email='myemail@gmail.com', 
                profile_picture='https://example.com/images/antogachie.jpg'
            )
            with pytest.raises(IntegrityError):
                db.session.add(student)
                db.session.commit()

    def test_requires_first_name(self):
        """Requires each record to have a first_name"""

        with app.app_context():
            Student.query.delete()
            db.session.commit()

            student = Student(
                username='antogachie', 
                last_name='Gachie', 
                email='myemail@gmail.com', 
                profile_picture='https://example.com/images/antogachie.jpg'
            )
            with pytest.raises(IntegrityError):
                db.session.add(student)
                db.session.commit()

    def test_requires_last_name(self):
        """Requires each record to have a last_name"""
        with app.app_context():
            Student.query.delete()
            db.session.commit()

            student = Student(
                username='antogachie', 
                first_name='Anthony',
                email='myemail@gmail.com', 
                profile_picture='https://example.com/images/antogachie.jpg'
            )
            with pytest.raises(IntegrityError):
                db.session.add(student)
                db.session.commit()

    def test_requires_email(self):
        """Requires each record to have an email"""
        with app.app_context():
            Student.query.delete()
            db.session.commit()

            student = Student(
                username='antogachie', 
                first_name='Anthony',
                last_name='Gachie', 
                profile_picture='https://example.com/images/antogachie.jpg'
            )
            with pytest.raises(IntegrityError):
                db.session.add(student)
                db.session.commit()

    def test_requires_profile_picture(self):
        """Requires each record to have a profile_picture"""
        with app.app_context():
            Student.query.delete()
            db.session.commit()

            student = Student(
                username='antogachie', 
                first_name='Anthony',
                last_name='Gachie', 
                email='myemail@gmail.com',
            )
            with pytest.raises(IntegrityError):
                db.session.add(student)
                db.session.commit()

    