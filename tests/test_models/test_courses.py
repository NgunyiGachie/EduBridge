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

            db.session.delete(new_course)
            db.session.commit()

    def test_requires_course_info(self):
        """Requires each record to have a course_info"""

        with app.app_context():
            Course.query.delete()
            db.session.commit

            try:
                course = Course(
                    instructor_id=1,
                    schedule=[
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ]
                )
                db.session.add(course)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                assert "course_info" in str(e), "course_info did not raise an error as expected"

    def test_requires_instructor_id(self):
        """Requires each record to have an instructor_id"""

        with app.app_context():
            Course.query.delete()
            db.session.commit()

            try:
                course = Course(
                    course_info="Biology for Dummies",
                    schedule=[
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ]
                )
                db.session.add(course)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "instructor_id" in str(e), "instructor_id validation did not raise an error as expected"

    def test_has_schedule(self):
        """Requires each record to have schedule"""

        with app.app_context():
            Course.query.delete()
            db.session.commit()

            try:
                course = Course(
                    course_info="Biology for Dummies",
                    instructor_id=1,
                )
                db.session.add(course)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "schedule" in str(e), "schedule validation did not raise an error as expected"

    def test_instructor_id_must_be_integer(self):
        """Requires instructor_id to be an integer"""

        with app.app_context():
            Course.query.delete()
            db.session.commit()

            try:
                course = Course(
                    course_info="Biology for Dummies",
                    instructor_id="one",
                    schedule=[
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ]
                )
                db.session.add(course)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "instructor_id" in str(e), "Non-integer instructor_id did not raise an error as expected"

    def test_course_info_must_be_string(self):
        """Requires course_info to be a string"""

        with app.app_context():
            Course.query.delete()
            db.session.commit()

            try:
                course = Course(
                    course_info=1,
                    instructor_id=1,
                    schedule=[
                    {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                    {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
                ]
                )
                db.session.add(course)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "course_info" in str(e), "Non-string course_info did not raise an error as expected"

    def test_schedule_must_be_list(self):
        """Requires schedule to be a list"""

        with app.app_context():
            Course.query.delete()
            db.session.commit()

            try:
                course = Course(
                    course_info="Biology for Dummies",
                    instructor_id=1,
                    schedule=datetime(2024, 6, 7)
                )
                db.session.add(course)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "schedule" in str(e), "Non-list schedule did not raise an error as expected"