import pytest
from app import app
from application.models.assignment import Assignment
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from database import db

class TestAssignment:
    """Test suite for the assignment model"""
    @pytest.fixture
    def setup_teardown(app):
        with app.app_context():
            db.create_all()
            yield
            db.session.rollback()
            db.drop_all()

    def test_has_attributes(self):
        """Has attributes title, description, course_id, due_date, total_points"""
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

            created_assignment = Assignment.query.filter(Assignment.title == "Introduction to Philosophy").first()
            assert created_assignment is not None
            assert created_assignment.title == "Introduction to Philosophy"
            assert created_assignment.description == "Explain the allegory of the cave"
            assert created_assignment.course_id == 1
            assert created_assignment.due_date == datetime(2024, 11, 16)
            assert created_assignment.total_points == 70
            assert created_assignment.id is not None

    def test_requires_title(self):
        """Requires each record to have a title"""
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
    
    def test_requires_description(self):
        """Requires each record to have a description"""
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

    def test_requires_course_id(self):
        """Requires each record to have a course_id"""
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

    def test_requires_due_date(self):
        """Requires each record to have a due_date"""
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

    def test_requires_total_points(self):
        """Requires each record to have total_points"""
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


    

