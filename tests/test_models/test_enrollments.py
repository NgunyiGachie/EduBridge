import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.enrollments import Enrollment

class TestEnrollments:
    """Test case for the Enrollment model"""
    @pytest.fixture
    def setup_teardown(app):
        with app.app_context():
            db.create_all()
            yield
            db.session.rollback()
            db.drop_all()

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

            enrollment = Enrollment(
                student_id=1, 
                status='enrolled'
                )
            with pytest.raises(IntegrityError):
                db.session.add(enrollment)
                db.session.commit()

    def test_requires_student_id(self):
        """Requires each record to have a student_id"""
        with app.app_context():
            Enrollment.query.delete()
            db.session.commit()

            enrollment = Enrollment(
                course_id=1, 
                status='enrolled'
                )
            with pytest.raises(IntegrityError):
                db.session.add(enrollment)
                db.session.commit()
        
    def test_requires_status(self):
        """Requires each record to have a status"""
        with app.app_context():
            Enrollment.query.delete()
            db.session.commit()

            enrollment = Enrollment(
                course_id=1, 
                student_id=1, 
                )
            with pytest.raises(IntegrityError):
                db.session.add(enrollment)
                db.session.commit()

   