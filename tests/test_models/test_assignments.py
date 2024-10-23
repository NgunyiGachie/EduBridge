import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.assignment import Assignment


class TestAssignment:
    """Test suite for the Assignment model."""

    @pytest.fixture
    def setup_teardown(self):
        """Set up and tear down the test database."""
        with app.app_context():
            db.create_all()
            yield
            db.session.rollback()
            db.drop_all()

    def test_has_attributes(self, setup_teardown):
        """Test that the assignment model has required attributes."""
        with app.app_context():
            Assignment.query.delete()
            db.session.commit()

            assignment = Assignment(
                title='Introduction to Philosophy',
                description='Explain the allegory of the cave',
                course_id=1,
                due_date=datetime(2024, 11, 16),
                total_points=70,
            )
            db.session.add(assignment)
            db.session.commit()

            created_assignment = Assignment.query.filter(
                Assignment.title == "Introduction to Philosophy").first()
            assert created_assignment is not None
            assert created_assignment.title == "Introduction to Philosophy"
            assert created_assignment.description == "Explain the allegory of the cave"
            assert created_assignment.course_id == 1
            assert created_assignment.due_date == datetime(2024, 11, 16)
            assert created_assignment.total_points == 70
            assert created_assignment.id is not None

    def test_requires_title(self, setup_teardown):
        """Test that the title is a required field."""
        with app.app_context():
            Assignment.query.delete()
            db.session.commit()

            assignment = Assignment(
                description='Explain the allegory of the cave',
                course_id=1,
                due_date=datetime(2024, 11, 16),
                total_points=70,
            )
            with pytest.raises(IntegrityError):
                db.session.add(assignment)
                db.session.commit()

    def test_requires_description(self, setup_teardown):
        """Test that the description is a required field."""
        with app.app_context():
            Assignment.query.delete()
            db.session.commit()

            assignment = Assignment(
                title='Introduction to Philosophy',
                course_id=1,
                due_date=datetime(2024, 11, 16),
                total_points=70,
            )
            with pytest.raises(IntegrityError):
                db.session.add(assignment)
                db.session.commit()

    def test_requires_course_id(self, setup_teardown):
        """Test that the course_id is a required field."""
        with app.app_context():
            Assignment.query.delete()
            db.session.commit()

            assignment = Assignment(
                title='Introduction to Philosophy',
                description='Explain the allegory of the cave',
                due_date=datetime(2024, 11, 16),
                total_points=70,
            )
            with pytest.raises(IntegrityError):
                db.session.add(assignment)
                db.session.commit()

    def test_requires_due_date(self, setup_teardown):
        """Test that the due_date is a required field."""
        with app.app_context():
            Assignment.query.delete()
            db.session.commit()

            assignment = Assignment(
                title='Introduction to Philosophy',
                description='Explain the allegory of the cave',
                course_id=1,
                total_points=70,
            )
            with pytest.raises(IntegrityError):
                db.session.add(assignment)
                db.session.commit()

    def test_requires_total_points(self, setup_teardown):
        """Test that total_points is a required field."""
        with app.app_context():
            Assignment.query.delete()
            db.session.commit()

            assignment = Assignment(
                title='Introduction to Philosophy',
                description='Explain the allegory of the cave',
                course_id=1,
                due_date=datetime(2024, 11, 16),
            )
            with pytest.raises(IntegrityError):
                db.session.add(assignment)
                db.session.commit()
