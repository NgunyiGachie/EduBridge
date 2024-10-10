import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.grades import Grade
from datetime import datetime

class TestGrades:
    """Test case for the grades model"""
    @pytest.fixture
    def setup_teardown(app):
        with app.app_context():
            db.create_all()
            yield
            db.session.rollback()
            db.drop_all()

    def test_has_attributes(self):
        """Requires the grades model to have attributes: student_id, course_id, grades, date_posted"""
        with app.app_context():
            Grade.query.delete()
            db.session.commit

            grade = Grade(
                student_id=1, 
                course_id=2, 
                grade=20, 
                date_posted=datetime(2024, 9, 1, 10, 0, 0)
            )
            db.session.add(grade)
            db.session.commit()

            new_grade = Grade.query.filter(Grade.id).first()
            assert new_grade is not None
            assert new_grade.student_id == 1
            assert new_grade.course_id == 2
            assert new_grade.grade == 20
            assert new_grade.date_posted == datetime(2024, 9, 1, 10, 0, 0)
            db.session.delete(new_grade)
            db.session.commit()

    def test_require_student_id(self):
        """Requires each record to have student_id"""
        with app.app_context():
            Grade.query.delete()
            db.session.commit()

            grade = Grade(
                course_id=2, 
                grade=20, 
                date_posted=datetime(2024, 9, 1, 10, 0, 0)
            )
            with pytest.raises(IntegrityError):
                db.session.add(grade)
                db.session.commit()

    def test_requires_course_id(self):
        """Requires each record to have a course_id"""
        with app.app_context():
            Grade.query.delete()
            db.session.commit()

            grade = Grade(
                student_id=1, 
                grade=20, 
                date_posted=datetime(2024, 9, 1, 10, 0, 0)
            )
            with pytest.raises(IntegrityError):
                db.session.add(grade)
                db.session.commit()

    def test_requires_grades(self):
        """Requirs each record to have grades"""
        with app.app_context():
            Grade.query.delete()
            db.session.commit()

            grade = Grade(
                student_id=1, 
                course_id=2, 
                date_posted=datetime(2024, 9, 1, 10, 0, 0)
            )
            with pytest.raises(IntegrityError):
                db.session.add(grade)
                db.session.commit()

    def test_requires_date_posted(self):
        """Requires each record to have date_posted"""
        with app.app_context():
            Grade.query.delete()
            db.session.commit()

            grade = Grade(
                student_id=1, 
                course_id=2, 
                grade=20, 
            )
            with pytest.raises(IntegrityError):
                db.session.add(grade)
                db.session.commit()

    