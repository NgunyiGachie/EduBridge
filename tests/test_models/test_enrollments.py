from app import app
from database import db
from application.models.enrollments import Enrollment

class TestEnrollments:
    """Test case for the Enrollment model"""

    def test_has_attributes(self):
        """Test enrollments model has attributes: course_id, student_id, status"""

        with app.app_context():
            Enrollment.query.delete()
            db.session.commit

            enrollment = Enrollment(
                course_id=1, 
                student_id=1, 
                status='enrolled'
                )
            db.session.add(enrollment)
            db.session.commit()

            new_enrollment = Enrollment.query.filter(Enrollment.id).first()
            assert new_enrollment is not None
            assert new_enrollment.course_id == 1
            assert new_enrollment.student_id == 1
            assert new_enrollment.status == 'enrolled'

            db.session.delete(new_enrollment)
            db.session.commit()

    def test_requires_course_id(self):
        """Requires each record to have a course_id"""

        with app.app_context():
            Enrollment.query.delete()
            db.session.commit()

            try:
                enrollment = Enrollment( 
                    student_id=1, 
                    status='enrolled'
                )
                db.session.add(enrollment)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "course_id" in str(e), "course_id validation did not raise an error as expected"

    def test_requires_student_id(self):
        """Requires each record to have a student_id"""

        with app.app_context():
            Enrollment.query.delete()
            db.session.commit()

            try:
                enrollment = Enrollment(
                    course_id=1, 
                    status='enrolled'
                )
                db.session.add(enrollment)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "student_id" in str(e), "student_id validation did not raise an error as expected"

    def test_requires_status(self):
        """Requires each record to have a status"""

        with app.app_context():
            Enrollment.query.delete()
            db.session.commit()

            try:
                enrollment = Enrollment(
                    course_id=1, 
                    student_id=1
                )
                db.session.add(enrollment)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "status" in str(e), "status validation did not raise an error as expected"

    def test_course_id_must_be_integer(self):
        """Requires course_id to be an integer"""

        with app.app_context():
            Enrollment.query.delete()
            db.session.commit()

            try:
                enrollment = Enrollment(
                    course_id="one", 
                    student_id=1, 
                    status='enrolled'
                )
                db.session.add(enrollment)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "course_id" in str(e), "Non-integer course_id did not raise an error as expected"

    def test_student_id_must_be_integer(self):
        """Requires student_id to be an integer"""

        with app.app_context():
            Enrollment.query.delete()
            db.session.commit()

            try:
                enrollment = Enrollment(
                    course_id=1, 
                    student_id="one", 
                    status='enrolled'
                )
                db.session.add(enrollment)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "student_id" in str(e), "Non-integer student_id did not raise an error as expected"

    def test_status_must_be_string(self):
        """Requires status to be a string"""

        with app.app_context():
            Enrollment.query.delete()
            db.session.commit()

            try:
                enrollment = Enrollment(
                    course_id=1, 
                    student_id=1, 
                    status=2
                )
                db.session.add(enrollment)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "status" in str(e), "Non-string status did not raise an error as expected"

    def test_invalid_status_values(self):
        """Rejects invalid status values"""

        with app.app_context():
            Enrollment.query.delete()
            db.session.commit()

            try:
                enrollment = Enrollment(
                    course_id=1, 
                    student_id=1, 
                    status='I am in'
                )
            except Exception as e:
                db.session.rollback()
                assert "status" in str(e), "Invalid status did not raise an error as expected"