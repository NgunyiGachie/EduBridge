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

    def test_string_values(self):
        """Requires username, first_name, last_name, email to be strings"""

        with app.app_context():
            Student.query.delete()
            db.session.commit()

            student_with_non_string_username = Student(
                username=1, 
                first_name='Anthony', 
                last_name='Gachie', 
                email='myemail@gmail.com', 
                profile_picture='https://example.com/images/antogachie.jpg'
            )
            with pytest.raises(ValueError, match="username must be a string"):
                db.session.add(student_with_non_string_username)
                db.session.commit()

            student_with_string_first_name = Student(
                username='antogachie', 
                first_name=1, 
                last_name='Gachie', 
                email='myemail@gmail.com', 
                profile_picture='https://example.com/images/antogachie.jpg'
            )
            with pytest.raises(ValueError, match="first_name must be a string"):
                db.session.add(student_with_string_first_name)
                db.session.commit()

            student_with_non_string_last_name = Student(
                username='antogachie', 
                first_name='Anthony', 
                last_name=1, 
                email='myemail@gmail.com', 
                profile_picture='https://example.com/images/antogachie.jpg'
            )
            with pytest.raises(ValueError, match="last_name must be a string"):
                db.session.add(student_with_non_string_last_name)
                db.session.commit()

            student_with_non_string_email = Student(
                username='antogachie', 
                first_name='Anthony', 
                last_name='Gachie', 
                email=1, 
                profile_picture='https://example.com/images/antogachie.jpg'
            )
            with pytest.raises(ValueError, match="email must be a string"):
                db.session.add(student_with_non_string_email)
                db.session.commit()

            student_with_non_string_profile_picture = Student(
                username='antogachie', 
                first_name='Anthony', 
                last_name='Gachie', 
                email='myemail@gmail.com', 
                profile_picture=1
            )
            with pytest.raises(ValueError, match="profile_picture must be a string"):
                db.session.add(student_with_non_string_profile_picture)
                db.session.commit()



    