"""Test suite for the Grade model."""

from datetime import datetime
import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.grades import Grade


@pytest.fixture
def setup_teardown():
    """Set up the database for testing and tear it down afterward."""
    with app.app_context():
        db.create_all()
        yield
        db.session.rollback()
        db.drop_all()


class TestGrades:
    """Test case for the Grade model."""

    @pytest.mark.usefixtures("setup_teardown")
    def test_has_attributes(self):
        """Test if the Grade model has required attributes."""
        with app.app_context():
            Grade.query.delete()
            db.session.commit()

            grade = Grade(
                student_id=1,
                course_id=2,
                grade=20,
                date_posted=datetime(2024, 9, 1, 10, 0, 0)
            )
            db.session.add(grade)
            db.session.commit()

            new_grade = Grade.query.filter_by(student_id=1).first()
            assert new_grade is not None
            assert new_grade.student_id == 1
            assert new_grade.course_id == 2
            assert new_grade.grade == 20
            assert new_grade.date_posted == datetime(2024, 9, 1, 10, 0, 0)

            db.session.delete(new_grade)
            db.session.commit()

    def test_requires_student_id(self):
        """Test that each record must have a student_id."""
        with app.app_context():
            Grade.query.delete()
            db.session.commit()

            grade = Grade(
                course_id=2,
                grade=20,
                date_posted=datetime(2024, 9, 1, 10, 0, 0)
            )
            with pytest.raises(IntegrityError):
                db.session.add(grade)
                db.session.commit()

    def test_requires_course_id(self):
        """Test that each record must have a course_id."""
        with app.app_context():
            Grade.query.delete()
            db.session.commit()

            grade = Grade(
                student_id=1,
                grade=20,
                date_posted=datetime(2024, 9, 1, 10, 0, 0)
            )
            with pytest.raises(IntegrityError):
                db.session.add(grade)
                db.session.commit()

    def test_requires_grades(self):
        """Test that each record must have a grade."""
        with app.app_context():
            Grade.query.delete()
            db.session.commit()

            grade = Grade(
                student_id=1,
                course_id=2,
                date_posted=datetime(2024, 9, 1, 10, 0, 0)
            )
            with pytest.raises(IntegrityError):
                db.session.add(grade)
                db.session.commit()

    def test_requires_date_posted(self):
        """Test that each record must have a date_posted."""
        with app.app_context():
            Grade.query.delete()
            db.session.commit()

            grade = Grade(
                student_id=1,
                course_id=2,
                grade=20
            )
            with pytest.raises(IntegrityError):
                db.session.add(grade)
                db.session.commit()
