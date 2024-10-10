import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.lectures import Lecture
from datetime import datetime

class TestLectures:
    """Test case for the lecture model"""
    @pytest.fixture
    def setup_teardown(app):
        with app.app_context():
            db.create_all()
            yield
            db.session.rollback()
            db.drop_all()

    def test_has__attributes(self):
        """Has attributes: lecture_info, instructor_id, schedule, created_at, updated_at"""
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
                created_at=datetime(2024, 9, 16),
                updated_at=datetime(2024, 9, 16)
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
            assert created_lecture.created_at == datetime(2024, 9, 16)
            assert created_lecture.updated_at == datetime(2024, 9, 16)

    def test_requires_lecture_info(self):
        """Requires each record to have lecture_info"""
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
                created_at=datetime(2024, 9, 16),
                updated_at=datetime(2024, 9, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(lecture)
                db.session.commit()

    def test_requires_instructor_id(self):
        """Requires each record to have instructor_id"""
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
                created_at=datetime(2024, 9, 16),
                updated_at=datetime(2024, 9, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(lecture)
                db.session.commit()

    def test_requires_schedule(self):
        """Requires each record to have schedule"""
        with app.app_context():
            Lecture.query.delete()
            db.session.commit()

            lecture = Lecture(
                lecture_info='ZOOL 102',
                instructor_id=1,
                created_at=datetime(2024, 9, 16),
                updated_at=datetime(2024, 9, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(lecture)
                db.session.commit()

    def test_requires_created_at(self):
        """Requires each record to have created_at"""
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
                updated_at=datetime(2024, 9, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(lecture)
                db.session.commit()

    def test_requires_updated_at(self):
        """Requires each record to have updated_at"""
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
                created_at=datetime(2024, 9, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(lecture)
                db.session.commit()

    