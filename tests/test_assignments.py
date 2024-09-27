import pytest
from app import app
from application.models.assignment import Assignment
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from database import db

@pytest.fixture
def setup_teardown(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.rollback()
        db.drop_all()

def test_assignment_creation_valid_data(setup_teardown):
    valid_due_date = datetime.now() + timedelta(days=1)
    assignment = Assignment(
        title="Assignment1",
        description="This is a valid assignment",
        course_id=1,
        due_date=valid_due_date,
        total_points=100
    )
    db.session.add(assignment)
    db.session.commit()

    assert assignment.id is not None
    assert assignment.title == "Assignment 1"
    assert assignment.description == "This is a valid assignment"
    assert assignment.due_date == valid_due_date
    assert assignment.total_points == 100

def test_invalid_title(setup_teardown):
    past_due_date = datetime.now() + timedelta(days=1)
    with pytest.raises(ValueError, match="Due date must be in the future"):
        Assignment(
            title="Assignment1",
            description="This is a valid assignment",
            course_id=1,
            due_date=past_due_date,
            total_points=100
        )

def test_invalid_total_points(setup_teardown):
    future_due_date = datetime.now() + timedelta(days=1)
    with pytest.raises(ValueError, match="Total points must be greater than or equal to zero"):
        Assignment(
            title="Assignment1",
            description="This is a valid assignment",
            course_id=1,
            due_date=future_due_date,
            total_points=100
        )

def test_assignment_with_none_total_points(setup_teardown):
    future_due_date = datetime.now() + timedelta(days=1)
    with pytest.raises(ValueError, match="Total points cannot be None"):
        Assignment(
            title="Assignment1",
            description="This is a valid assignment",
            course_id=1,
            due_date=future_due_date,
            total_points=100
        )
        
        
    

