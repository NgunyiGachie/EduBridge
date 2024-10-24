"""Test suite for the Notification model"""

from datetime import datetime
import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.notifications import Notification

class TestNotification:
    """Test case for the Notification model."""

    @pytest.fixture
    def setup_teardown(self):
        """Setup and teardown for the test case."""
        with app.app_context():
            db.create_all()
            yield
            db.session.rollback()
            db.drop_all()

    def test_has_attributes(self):
        """Test that Notification has the correct attributes."""
        with app.app_context():
            Notification.query.delete()
            db.session.commit()

            notification = Notification(
                title='Class is at ten',
                message_body='Please attend the class',
                student_id=1,
                instructor_id=1,
                read_status='read',
                sent_date=datetime(2024, 9, 1, 9, 0, 0),
                read_date=datetime(2024, 9, 1, 9, 0, 0),
            )
            db.session.add(notification)
            db.session.commit()

            created_notification = Notification.query.filter_by(title="Class is at ten").first()
            assert created_notification is not None
            assert created_notification.title == "Class is at ten"
            assert created_notification.message_body == "Please attend the class"
            assert created_notification.student_id == 1
            assert created_notification.instructor_id == 1
            assert created_notification.read_status == "read"
            assert created_notification.sent_date == datetime(2024, 9, 1, 9, 0, 0)
            assert created_notification.read_date == datetime(2024, 9, 1, 9, 0, 0)
            db.session.delete(created_notification)
            db.session.commit()

    def test_requires_title(self):
        """Test that each Notification requires a title."""
        with app.app_context():
            notification = Notification(
                message_body='Please attend the class',
                student_id=3,
                instructor_id=2,
                read_status='read',
                sent_date=datetime(2024, 9, 1, 9, 0, 0),
                read_date=datetime(2024, 9, 1, 9, 0, 0),
            )
            with pytest.raises(IntegrityError):
                db.session.add(notification)
                db.session.commit()

    def test_requires_message_body(self):
        """Test that each Notification requires a message body."""
        with app.app_context():
            notification = Notification(
                title='Class is at ten',
                student_id=3,
                instructor_id=2,
                read_status='read',
                sent_date=datetime(2024, 9, 1, 9, 0, 0),
                read_date=datetime(2024, 9, 1, 9, 0, 0),
            )
            with pytest.raises(IntegrityError):
                db.session.add(notification)
                db.session.commit()

    def test_requires_student_id(self):
        """Test that each Notification requires a student ID."""
        with app.app_context():
            notification = Notification(
                title='Class is at ten',
                message_body='Please attend the class',
                instructor_id=2,
                read_status='read',
                sent_date=datetime(2024, 9, 1, 9, 0, 0),
                read_date=datetime(2024, 9, 1, 9, 0, 0),
            )
            with pytest.raises(IntegrityError):
                db.session.add(notification)
                db.session.commit()

    def test_requires_instructor_id(self):
        """Test that each Notification requires an instructor ID."""
        with app.app_context():
            notification = Notification(
                title='Class is at ten',
                message_body='Please attend the class',
                student_id=3,
                read_status='read',
                sent_date=datetime(2024, 9, 1, 9, 0, 0),
                read_date=datetime(2024, 9, 1, 9, 0, 0),
            )
            with pytest.raises(IntegrityError):
                db.session.add(notification)
                db.session.commit()

    def test_requires_read_status(self):
        """Test that each Notification requires a read status."""
        with app.app_context():
            notification = Notification(
                title='Class is at ten',
                message_body='Please attend the class',
                student_id=3,
                instructor_id=2,
                sent_date=datetime(2024, 9, 1, 9, 0, 0),
                read_date=datetime(2024, 9, 1, 9, 0, 0),
            )
            with pytest.raises(IntegrityError):
                db.session.add(notification)
                db.session.commit()

    def test_requires_sent_date(self):
        """Test that each Notification requires a sent date."""
        with app.app_context():
            notification = Notification(
                title='Class is at ten',
                message_body='Please attend the class',
                student_id=3,
                instructor_id=2,
                read_status='read',
                read_date=datetime(2024, 9, 1, 9, 0, 0),
            )
            with pytest.raises(IntegrityError):
                db.session.add(notification)
                db.session.commit()

    def test_requires_read_date(self):
        """Test that each Notification requires a read date."""
        with app.app_context():
            notification = Notification(
                title='Class is at ten',
                message_body='Please attend the class',
                student_id=3,
                instructor_id=2,
                read_status='read',
                sent_date=datetime(2024, 9, 1, 9, 0, 0),
            )
            with pytest.raises(IntegrityError):
                db.session.add(notification)
                db.session.commit()
