import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.course import Course
from datetime import datetime

class TestCourse:
    """Test case for the Course model"""

    def test_has_attributes(self):
        """Test course model has attributes: course_info, instructor_id, schedule"""

        with app.app_context():
            Course.query.delete()
            db.session.commit

            course = Course(
                course_info="Biology for Dummies",
                instructor_id=1,
                schedule=[
                {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
            ]
            )
            db.session.add(course)
            db.session.commit()

            new_course = Course.query.filter(Course.id).first()
            assert new_course is not None
            assert new_course.course_info == "Biology for Dummies"
            assert new_course.instructor_id == 1
            assert new_course.schedule == [
                {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
            ]
            assert new_course.id is not None

    def test_requires_course_info(self):
        """Requires each record to have a course_info"""
        with app.app_context():
            Course.query.delete()
            db.session.commit

            course = Course(
                instructor_id=1,
                schedule=[
                {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
            ]
            )
            with pytest.raises(IntegrityError):
                db.session.add(course)
                db.session.commit()

    def test_requires_instructor_id(self):
        """Requires each record to have an instructor_id"""
        with app.app_context():
            Course.query.delete()
            db.session.commit()

            course = Course(
                course_info="Biology for Dummies",
                schedule=[
                {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
            ]
            )
            with pytest.raises(IntegrityError):
                db.session.add(course)
                db.session.commit()
           
    def test_has_schedule(self):
        """Requires each record to have schedule"""
        with app.app_context():
            Course.query.delete()
            db.session.commit()

            course = Course(
                course_info="Biology for Dummies",
                instructor_id=1,
            )
            with pytest.raises(IntegrityError):
                db.session.add(course)
                db.session.commit()

   