import datetime  # Move datetime import up
import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.lectures import Lecture

class TestLectures:
    """Test case for the lecture model."""

    @pytest.fixture
    def setup_teardown(self):  # Add self as first argument
        with app.app_context():
            db.create_all()
            yield
            db.session.rollback()
            db.drop_all()

    def test_has_attributes(self):
        """Test that the lecture has the required attributes."""
        with app.app_context():
            Lecture.query.delete()
            db.session.commit()

            lecture = Lecture(
                lecture_info='ZOOL 102',
                instructor_id=1,
                schedule=[
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ],
                created_at=datetime.datetime(2024, 9, 16),
                updated_at=datetime.datetime(2024, 9, 16)
            )
            db.session.add(lecture)
            db.session.commit()

            created_lecture = Lecture.query.filter(Lecture.lecture_info == 'ZOOL 102').first()
            assert created_lecture is not None
            assert created_lecture.lecture_info == 'ZOOL 102'
            assert created_lecture.instructor_id == 1
            assert created_lecture.schedule == [
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ]
            assert created_lecture.created_at == datetime.datetime(2024, 9, 16)
            assert created_lecture.updated_at == datetime.datetime(2024, 9, 16)

    def test_requires_lecture_info(self):
        """Test that lecture_info is required."""
        with app.app_context():
            Lecture.query.delete()
            db.session.commit()

            lecture = Lecture(
                instructor_id=1,
                schedule=[
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ],
                created_at=datetime.datetime(2024, 9, 16),
                updated_at=datetime.datetime(2024, 9, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(lecture)
                db.session.commit()

    def test_requires_instructor_id(self):
        """Test that instructor_id is required."""
        with app.app_context():
            Lecture.query.delete()
            db.session.commit()

            lecture = Lecture(
                lecture_info='ZOOL 102',
                schedule=[
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ],
                created_at=datetime.datetime(2024, 9, 16),
                updated_at=datetime.datetime(2024, 9, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(lecture)
                db.session.commit()

    def test_requires_schedule(self):
        """Test that schedule is required."""
        with app.app_context():
            Lecture.query.delete()
            db.session.commit()

            lecture = Lecture(
                lecture_info='ZOOL 102',
                instructor_id=1,
                created_at=datetime.datetime(2024, 9, 16),
                updated_at=datetime.datetime(2024, 9, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(lecture)
                db.session.commit()

    def test_requires_created_at(self):
        """Test that created_at is required."""
        with app.app_context():
            Lecture.query.delete()
            db.session.commit()

            lecture = Lecture(
                lecture_info='ZOOL 102',
                instructor_id=1,
                schedule=[
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ],
                updated_at=datetime.datetime(2024, 9, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(lecture)
                db.session.commit()

    def test_requires_updated_at(self):
        """Test that updated_at is required."""
        with app.app_context():
            Lecture.query.delete()
            db.session.commit()

            lecture = Lecture(
                lecture_info='ZOOL 102',
                instructor_id=1,
                schedule=[
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ],
                created_at=datetime.datetime(2024, 9, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(lecture)
                db.session.commit()
