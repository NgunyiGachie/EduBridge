import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.notifications import Notification
from datetime import datetime

class TestNotification:
    """Test case for the notification model"""

    def test_has_attributes(self):
        """has attributes: title, message_body, student_id, read_status, sent_date, read_date"""

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
                read_date=datetime(2024, 9, 1, 9, 0, 0),
            )
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

    def test_requires_title(self):
        """Requires each record to have title"""

        with app.app_context():
            Notification.query.delete()
            db.session.commit()

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
                db.session.add

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
            db.session.add()

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

    def test_string_values(self):
        """Requires title and message_body to be a string"""

        with app.app_context():
            Notification.query.delete()
            db.session.commit()

            notification_with_non_string_title = Notification(
                title=1,
                message_body='Please attend the class',
                student_id=3, 
                instructor_id=2, 
                read_status='read', 
                sent_date=datetime(2024, 9, 1, 9, 0, 0), 
                read_date=datetime(2024, 9, 1, 9, 0, 0),
            )
            with pytest.raises(ValueError, match="Title must be a string"):
                db.session.add(notification_with_non_string_title)
                db.session.commit

            notification_with_non_string_message_body = Notification(
                title='Class is at ten', 
                message_body=2,
                student_id=3, 
                instructor_id=2, 
                read_status='read', 
                sent_date=datetime(2024, 9, 1, 9, 0, 0), 
                read_date=datetime(2024, 9, 1, 9, 0, 0),
            )
            with pytest.raises(ValueError, match="Message_body must be a string"):
                db.session.add(notification_with_non_string_message_body)
                db.session.commit()

    def test_integer_value(self):
        """Requires student_id and instructor_id to be integers"""

        with app.app_context():
            Notification.query.delete()
            db.session.commit()

            notification_with_non_integer_student_id = Notification(
                title='Class is at ten', 
                message_body='Please attend the class',
                student_id="3", 
                instructor_id=2, 
                read_status='read', 
                sent_date=datetime(2024, 9, 1, 9, 0, 0), 
                read_date=datetime(2024, 9, 1, 9, 0, 0),
            )
            with pytest.raises(ValueError, match="Student_id must be an integer"):
                db.session.add(notification_with_non_integer_student_id)
                db.session.commit()

            notification_with_non_integer_instructor_id = Notification(
                title='Class is at ten', 
                message_body='Please attend the class',
                student_id=3, 
                instructor_id="2", 
                read_status='read', 
                sent_date=datetime(2024, 9, 1, 9, 0, 0), 
                read_date=datetime(2024, 9, 1, 9, 0, 0),
            )
            with pytest.raises(ValueError, match="Instructor_id must be an integer"):
                db.session.add(notification_with_non_integer_instructor_id)
                db.session.commit()
    
    def test_dates(self):
        """Test requires date values to not be in the future"""

        with app.app_context():
            Notification.query.delete()
            db.session.commit()

            notification_with_future_sent_date = Notification(
                title='Class is at ten', 
                message_body='Please attend the class',
                student_id=3, 
                instructor_id=2, 
                read_status='read', 
                sent_date=datetime(2050, 9, 1, 9, 0, 0), 
                read_date=datetime(2024, 9, 1, 9, 0, 0),
            )
            with pytest.raises(ValueError, match="Sent_date cannot be in the future"):
                db.session.add(notification_with_future_sent_date)
                db.session.commit()

            notification_with_future_read_date = Notification(
                title='Class is at ten', 
                message_body='Please attend the class',
                student_id=3, 
                instructor_id=2, 
                read_status='read', 
                sent_date=datetime(2024, 9, 1, 9, 0, 0), 
                read_date=datetime(2050, 9, 1, 9, 0, 0),
            )
            with pytest.raises(ValueError, match="Read_date cannot be in the future"):
                db.session.add(notification_with_future_read_date)
                db.session.commit()
        

    
        