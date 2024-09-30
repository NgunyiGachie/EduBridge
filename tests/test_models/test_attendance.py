from app import app
from database import db
from application.models.attendance import Attendance
from datetime import datetime

class TestAttendance:
    """Test case for the attendance model"""

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
                date=datetime(2024, 7, 16)
            )

            db.session.add(attendance)
            db.session.commit()

            new_attendance = Attendance.query.filter(Attendance.id).first()
            assert new_attendance is not None
            assert new_attendance.student_id == 1
            assert new_attendance.lecture_id == 1
            assert new_attendance.attendance_status == 'present'
            assert new_attendance.date == datetime(2024, 7, 16)

            db.session.delete(new_attendance)
            db.session.commit()
            
    def test_requires_student_id(self):
        """Requires each record to have a student_id"""

        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            try:
                attendance = Attendance(
                    lecture_id=1,
                    instructor_id=1,
                    attendance_status=1,
                    attendance_status="present",
                    date=datetime(2024, 7, 16)
                )
                db.session.add(attendance)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "student_id" in str(e), "student_id validation did not raise an error as expected"

    def test_requires_lecture_id(self):
        """Requires each record to have a lecture_id"""

        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            try:
                attendance = Attendance(
                    student_id=1,
                    instructor_id=1,
                    attendance_status=1,
                    attendance_status="present",
                    date=datetime(2024, 7, 16)
                )
                db.session.add(attendance)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "lecture_id" in str(e), "lecture_id validation did not raise an error as expected"

    def test_requires_instructor_id(self):
        """Requires each record to have an instructor_id"""

        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            try:
                attendance = Attendance(
                    lecture_id=1,
                    instructor_id=1,
                    attendance_status=1,
                    attendance_status="present",
                    date=datetime(2024, 7, 16)
                )
                db.session.add(attendance)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "instructor_id" in str(e), "instructor_id validation did not raise an error as expected"
    
    def test_student_id_must_be_integer(self):
        """Requires student_id to be an integer"""
        
        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            try:
                attendance = Attendance(
                    student_id="one", 
                    lecture_id=1,
                    instructor_id=1,
                    attendance_status="present",
                    date=datetime(2024, 7, 16)
                )
                db.session.add(attendance)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
            assert "student_id" in str(e), "Non-integer student_id did not raise an error"

    def test_lecture_id_must_be_integer(self):
        """Requires lecture_id to be an integer"""
        
        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            try:
                attendance = Attendance(
                    student_id=1, 
                    lecture_id="one",
                    instructor_id=1,
                    attendance_status="present",
                    date=datetime(2024, 7, 16)
                )
                db.session.add(attendance)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "lecture_id" in str(e), "Non-integer lecture_id did not raise an error"

    def test_instructor_id_must_be_integer(self):
        """Requires instructor_id to be an integer"""
        
        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            try:
                attendance = Attendance(
                    student_id=1,
                    lecture_id=1,
                    instructor_id="one",
                    attendance_status="present",
                    date=datetime(2024, 7, 16)
                )
                db.session.add(attendance)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "instructor_id" in str(e), "Non-integer instructor_id did not raise an error"

            
    def test_invalid_attendance_status(self):
        """ Rejects invalid attendance_status values"""

        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            try:
                attendance= Attendance(
                    student_id=1,
                    lecture_id=1,
                    instructor_id=1,
                    attendance_status="invalid status",
                    date=datetime(2024, 7, 16)
                    )
                db.session.add(attendance)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "attendance_status" in str(e), "Invalid attendance_status did not raise an error as expected"

    def test_invalide_date(self):
        """Rejects future dates"""

        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            future_date = datetime(2030, 1, 1)
            try:
                attendance = Attendance(
                    student_id=1,
                    lecture_id=1,
                    instructor_id=1,
                    attendance_status="present",
                    date=future_date
                )
                db.session.add(attendance)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "date" in str(e), "Future date did not raise an error as expected"

    def test_duplicate_attendance(self):
        """Rejects duplicate attendance records for the same student and lecture"""
        
        with app.app_context():
            Attendance.query.delete()
            db.session.commit()

            attendance = Attendance(
                student_id=1,
                lecture_id=1,
                instructor_id=1,
                attendance_status="present",
                date=datetime(2024, 7, 16)
            )
            db.session.add(attendance)
            db.session.commit()

            try:
                duplicate_attendance = Attendance(
                    student_id=1,
                    lecture_id=1,
                    instructor_id=1,
                    attendance_status="present",
                    date=datetime(2024, 7, 16)
                )
                db.session.add(duplicate_attendance)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "UNIQUE constraint failed" in str(e), "Duplicate attendance record did not raise an error"


        