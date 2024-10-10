import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.notifications import Notification
from application.models.students import Student
from application.models.instructors import Instructor
from datetime import datetime

class TestNotification:
    """Test case for the notification model"""
    @pytest.fixture
    def setup_teardown(app):
        with app.app_context():
            db.create_all()
            yield
            db.session.rollback()
            db.drop_all()

    def test_has_attributes(self):
        """has attributes: title, message_body, student_id, instructor_id, read_status, sent_date, read_date"""
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
            print(f"title: {notification.title}, message_body: {notification.message_body}, "
              f"student_id: {notification.student_id}, instructor_id: {notification.instructor_id}")
            db.session.add(notification)
            db.session.commit()

            created_notification = Notification.query.filter(Notification.title == "Class is at ten").first()
            assert created_notification is not None
            assert created_notification.title == "Class is at ten"
            assert created_notification.message_body == "Please attend the class"
            assert created_notification.student_id == 3
            assert created_notification.instructor_id == 2
            assert created_notification.read_status == "read"
            assert created_notification.sent_date == datetime(2024, 9, 1, 9, 0, 0)
            assert created_notification.read_date == datetime(2024, 9, 1, 9, 0, 0)
            db.session.delete(created_notification)
            db.session.commit()

    def test_requires_title(self):
        """Requires each record to have title"""
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
        """Requires each record to have a message_body"""
        with app.app_context():
            Notification.query.delete()
            db.session.commit()

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
        """Requires each record to have a student_id"""
        with app.app_context():
            Notification.query.delete()
            db.session.commit()

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
        """Requires each record to have an instructor id"""
        with app.app_context():
            Notification.query.delete()
            db.session.commit()

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
        """"Requires each record to have a read_status"""
        with app.app_context():
            Notification.query.delete()
            db.session.commit()

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
        """Requires each record to have a sent_date"""
        with app.app_context():
            Notification.query.delete()
            db.session.commit()

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
        """Requires each record to have read_date """
        with app.app_context():
            Notification.query.delete()
            db.session.commit()

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

    