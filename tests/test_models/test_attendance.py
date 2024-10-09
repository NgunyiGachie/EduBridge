import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.attendance import Attendance
from datetime import datetime

class TestAttendance:
    """Test case for the attendance model"""
    @pytest.fixture
    def setup_teardown(app):
        with app.app_context():
            db.create_all()
            yield
            db.session.rollback()
            db.drop_all()

    def test_has_attributes(self):
        """Test attendance model has attributes: student_id, lecture_id, instructor_id, attendance_status, date"""
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
            
    def test_requires_student_id(self):
        """Requires each record to have a student_id"""
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
            

    def test_requires_lecture_id(self):
        """Requires each record to have a lecture_id"""
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

    def test_requires_instructor_id(self):
        """Requires each record to have an instructor_id"""
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

    def test_requires_attendance_status(self):
        """Requires each record to have attendance_status"""
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

    def test_requires_date(self):
        """Requires each record to have a date"""
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
    
            
    

        