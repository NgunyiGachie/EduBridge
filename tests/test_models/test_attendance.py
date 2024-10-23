import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.attendance import Attendance


class TestAttendance:
    """Test case for the Attendance model."""

    @pytest.fixture
    def setup_teardown(self):
        """Set up and tear down the test database."""
        with app.app_context():
            db.create_all()
            yield
            db.session.rollback()
            db.drop_all()

    def test_has_attributes(self, setup_teardown):
        """Test that the attendance model has required attributes."""
        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            attendance = Attendance(
                student_id=1,
                lecture_id=1,
                instructor_id=1,
                attendance_status="present",
                dates=datetime(2024, 7, 16)
            )

            db.session.add(attendance)
            db.session.commit()

            new_attendance = Attendance.query.filter(Attendance.id).first()
            assert new_attendance is not None
            assert new_attendance.student_id == 1
            assert new_attendance.lecture_id == 1
            assert new_attendance.attendance_status == 'present'
            assert new_attendance.dates == datetime(2024, 7, 16)

            db.session.delete(new_attendance)
            db.session.commit()

    def test_requires_student_id(self, setup_teardown):
        """Test that the student_id is a required field."""
        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            attendance = Attendance(
                lecture_id=1,
                instructor_id=1,
                attendance_status="present",
                dates=datetime(2024, 7, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(attendance)
                db.session.commit()

    def test_requires_lecture_id(self, setup_teardown):
        """Test that the lecture_id is a required field."""
        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            attendance = Attendance(
                student_id=1,
                instructor_id=1,
                attendance_status="present",
                dates=datetime(2024, 7, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(attendance)
                db.session.commit()

    def test_requires_instructor_id(self, setup_teardown):
        """Test that the instructor_id is a required field."""
        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            attendance = Attendance(
                student_id=1,
                lecture_id=1,
                attendance_status="present",
                dates=datetime(2024, 7, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(attendance)
                db.session.commit()

    def test_requires_attendance_status(self, setup_teardown):
        """Test that the attendance_status is a required field."""
        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            attendance = Attendance(
                student_id=1,
                lecture_id=1,
                instructor_id=1,
                dates=datetime(2024, 7, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(attendance)
                db.session.commit()

    def test_requires_date(self, setup_teardown):
        """Test that the date is a required field."""
        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            attendance = Attendance(
                student_id=1,
                lecture_id=1,
                instructor_id=1,
                attendance_status="present",
            )
            with pytest.raises(IntegrityError):
                db.session.add(attendance)
                db.session.commit()
