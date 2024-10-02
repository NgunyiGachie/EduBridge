import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.instructors import Instructor
from argon2 import PasswordHasher

ph = PasswordHasher()

class TestInstructor:
    """Test case for instructor model"""

    def test_has_attributes(self):
        """Has attributes: name, email, password_hash, profile_picture, department, bio"""

        with app.app_context():
            Instructor.query.delete()
            db.session.commit()

            instructor = Instructor(
                name='Anthony', 
                email='instructor1@gmail.com',
                profile_picture='https://example.com/images/anthony.jpg', 
                department='Chemistry', 
                bio='Professor in Organic Chemistry'
            )
            instructor.password_hash = ph.hash("whosafraidofvirginiawoolf")

            db.session.add(instructor)
            db.session.commit()

            created_instructor = Instructor.query.filter(Instructor.name == "Anthony").first()

            assert created_instructor is not None
            assert created_instructor.name == "Anthony"
            assert created_instructor.email == "instructor1@gmail.com"
            assert created_instructor.profile_picture == "https://example.com/images/anthony.jpg"
            assert created_instructor.department == "Chemistry"
            assert created_instructor.bio == "Professor in Organic Chemistry"
            assert created_instructor.password_hash is not None

    def test_requires_name(self):
        """Requires each record to have a name"""

        with app.app_context():
            Instructor.query.delete()
            db.session.commit()

            instructor = Instructor(
                email='instructor1@gmail.com',
                profile_picture='https://example.com/images/anthony.jpg', 
                department='Chemistry', 
                bio='Professor in Organic Chemistry'
            )
            with pytest.raises(IntegrityError):
                db.session.add(instructor)
                db.session.commit()

    def test_requires_email(self):
        """Requires each record to have an email"""

        with app.app_context():
            Instructor.query.delete()
            db.session.commit()

            instructor = Instructor(
                name='Anthony', 
                profile_picture='https://example.com/images/anthony.jpg', 
                department='Chemistry', 
                bio='Professor in Organic Chemistry'
            )
            with pytest.raises(IntegrityError):
                db.session.add(instructor)
                db.session.commit()

    def test_requires_password_hash(self):
        """Requires each record to have a password_hash"""

        with app.app_context():
            Instructor.query.delete()
            db.session.commit()

            instructor = Instructor(
                name='Anthony', 
                email='instructor1@gmail.com',
                profile_picture='https://example.com/images/anthony.jpg', 
                department='Chemistry', 
                bio='Professor in Organic Chemistry'
            )
            with pytest.raises(IntegrityError):
                db.session.add(instructor)
                db.session.commit()

            instructor.password_hash = ph.hash("password123")
            db.session.add(instructor)
            db.session.commit()

            created_instructor = Instructor.query.filter(Instructor.email== 'instructor1@gmail.com').first()
            assert created_instructor is not None
            assert ph.verify(created_instructor.password_hash, "password123")

    def test_requires_profile_picture(self):
        """Requires each record to have a profile_picture"""

        with app.app_context():
            Instructor.query.delete()
            db.session.commit()

            instructor = Instructor(
                name='Anthony', 
                email='instructor1@gmail.com',
                department='Chemistry', 
                bio='Professor in Organic Chemistry'
            )
            with pytest.raises(IntegrityError):
                db.session.add(instructor)
                db.session.commit()

    def test_requires_department(self):
        """Requires each record to have a department"""

        with app.app_context():
            Instructor.query.delete()
            db.session.commit()

            instructor = Instructor(
                name='Anthony', 
                email='instructor1@gmail.com',
                profile_picture='https://example.com/images/anthony.jpg', 
                bio='Professor in Organic Chemistry'
            )
            with pytest.raises(IntegrityError):
                db.session.add(instructor)
                db.session.commit()

    def test_requires_bio(self):
        """Requires each record to have a bio"""

        with app.app_context():
            Instructor.query.delete()
            db.session.commit()

            instructor = Instructor(
                name='Anthony', 
                email='instructor1@gmail.com',
                profile_picture='https://example.com/images/anthony.jpg', 
                department='Chemistry'
            )
            with pytest.raises(IntegrityError):
                db.session.add(instructor)
                db.session.commit

    def test_invalid_email_format(self):
        """Tests if emails have the right format"""

        with app.app_context():
            Instructor.query.delete()
            db.session.commit()

            invalid_email = 'notemail'
            instructor = Instructor(
                name='Anthony', 
                email=invalid_email,
                profile_picture='https://example.com/images/anthony.jpg', 
                department='Chemistry', 
                bio='Professor in Organic Chemistry'
            )
            with pytest.raises(ValueError, match="Invalid mail format"):
                db.session.add(instructor)
                db.session.commit()

    def test_string_fields_must_be_strings(self):
        """Requires name, department, bio, and profile_picture to be strings"""

        with app.app_context():
            Instructor.query.delete()
            db.session.commit()

            instructor_with_invalid_name = Instructor(
                name=1,  
                email='instructor1@gmail.com',
                profile_picture='https://example.com/images/anthony.jpg',
                department='Chemistry',
                bio='Professor in Organic Chemistry'
            )
            with pytest.raises(ValueError, match="name must be a string"):
                db.session.add(instructor_with_invalid_name)
                db.session.commit()

            instructor_with_invalid_department = Instructor(
                name='Anthony',
                email='instructor2@gmail.com',
                profile_picture='https://example.com/images/anthony.jpg',
                department=101,  
                bio='Professor in Organic Chemistry'
            )
            with pytest.raises(ValueError, match="department must be a string"):
                db.session.add(instructor_with_invalid_department)
                db.session.commit()

            instructor_with_invalid_bio = Instructor(
                name='Anthony',
                email='instructor3@gmail.com',
                profile_picture='https://example.com/images/anthony.jpg',
                department='Chemistry',
                bio=1234  
            )
            with pytest.raises(ValueError, match="bio must be a string"):
                db.session.add(instructor_with_invalid_bio)
                db.session.commit()

            instructor_with_invalid_profile_picture = Instructor(
                name='Anthony',
                email='instructor4@gmail.com',
                profile_picture=404, 
                department='Chemistry',
                bio='Professor in Organic Chemistry'
            )
            with pytest.raises(ValueError, match="profile_picture must be a string"):
                db.session.add(instructor_with_invalid_profile_picture)
                db.session.commit()

