"""Test suite for the Instructor model"""

import pytest
from sqlalchemy.exc import IntegrityError
from argon2 import PasswordHasher
from app import app
from database import db
from application.models.instructors import Instructor

ph = PasswordHasher()

@pytest.fixture
def setup_teardown():
    """Set up the database for testing and tear it down afterward."""
    with app.app_context():
        db.create_all()
        yield
        db.session.rollback()
        db.drop_all()

class TestInstructor:
    """Test case for the Instructor model."""

    @pytest.mark.usefixtures("setup_teardown")
    def test_has_attributes(self):
        """Test if Instructor has the necessary attributes."""
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
        """Requires each record to have a name."""
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
        """Requires each record to have an email."""
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
        """Requires each record to have a password hash."""
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

            db.session.rollback()

            instructor.password_hash = ph.hash("password123")
            db.session.add(instructor)
            db.session.commit()

            created_instructor = Instructor.query.filter(Instructor.email == 'instructor1@gmail.com').first()
            assert created_instructor is not None
            assert ph.verify(created_instructor.password_hash, "password123")

    def test_requires_profile_picture(self):
        """Requires each record to have a profile picture."""
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
        """Requires each record to have a department."""
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
        """Requires each record to have a bio."""
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
                db.session.commit()
