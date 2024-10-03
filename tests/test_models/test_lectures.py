import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.lectures import Lecture
from datetime import datetime

class TestLectures:
    """Test case for the lecture model"""

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

    def test_lecture_info_must_be_string(self):
        """Requires lecture_info to be a string"""

        with app.app_context():
            Lecture.query.delete()
            db.session.commit()

            lecture = Lecture(
                lecture_info=1,
                instructor_id=1, 
                schedule=[
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ],
                created_at=datetime(2024, 9, 16),
                updated_at=datetime(2024, 9, 16)
            )
            with pytest.raises(ValueError, match="Lecture_info must be a string"):
                db.session.add(lecture)
                db.session.commit()

    def test_instructor_id_must_be_integer(self):
        """Requires instructor_id to be an integer"""

        with app.app_context():
            Lecture.query.delete()
            db.session.commit()

            lecture = Lecture(
                lecture_info='ZOOL 102',
                instructor_id="one", 
                schedule=[
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ],
                created_at=datetime(2024, 9, 16),
                updated_at=datetime(2024, 9, 16)
            )
            with pytest.raises(ValueError, match="Instructor_id must be an integer"):
                db.session.add(lecture)
                db.session.commit()

    def test_datetime_fields_must_not_be_in_future(self):
        """Requires datetime fields to not be in the future"""

        with app.app_context():
            Lecture.query.delete()
            db.session.commit()

            lecture_with_invalid_created_at = Lecture(
                lecture_info='ZOOL 102',
                instructor_id=1, 
                schedule=[
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ],
                created_at=datetime(2040, 5, 10),
                updated_at=datetime(2024, 9, 16)
            )
            with pytest.raises(ValueError, match="created_at cannot be in the future"):
                db.session.add(lecture_with_invalid_created_at)
                db.session.commit()

            lecture_with_invalid_updated_at = Lecture(
                lecture_info='ZOOL 102',
                instructor_id=1, 
                schedule=[
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ],
                created_at=datetime(2024, 9, 16),
                updated_at=datetime(2040, 9, 16)
            )
            with pytest.raises(ValueError, match="updated_at cannot be in the future"):
                db.session.add(lecture_with_invalid_updated_at)
                db.session.commit()
    
    def test_schedule_must_be_list(self):
        """Requires schedule to be a list"""

        with app.app_context():
            Lecture.query.delete()
            db.session.commit()

            lecture = Lecture(
                lecture_info='ZOOL 102',
                instructor_id=1, 
                schedule="Monday in the morning",
                created_at=datetime(2024, 9, 16),
                updated_at=datetime(2024, 9, 16)
            )
            with pytest.raises(ValueError, match="Schedule must be a list"):
                db.session.add(lecture)
                db.session.commit()
        