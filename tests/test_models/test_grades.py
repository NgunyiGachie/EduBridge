from app import app
from database import db
from application.models.grades import Grade
from datetime import datetime

class TestGrades:
    """Test case for the grades model"""

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

            try:
                grade = Grade(
                    course_id=2, 
                    grade=20, 
                    date_posted=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(grade)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "student_id" in str(e), "student_id validation did not raise an error as expected"

    def test_requires_course_id(self):
        """Requires each record to have a course_id"""

        with app.app_context():
            Grade.query.delete()
            db.session.commit()

            try:
                grade = Grade(
                    student_id=1,  
                    grade=20, 
                    date_posted=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(grade)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "course_id" in str(e), "course_id validation did not raise an error as expected"

    def test_requires_grades(self):
        """Requirs each record to have grades"""

        with app.app_context():
            Grade.query.delete()
            db.session.commit()

            try:
                grade = Grade(
                    student_id=1, 
                    course_id=2, 
                    date_posted=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(grade)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "grade" in str(e), "grade validation did not raise an error as expected"

    def test_requires_date_posted(self):
        """Requires each record to have date_posted"""

        with app.app_context():
            Grade.query.delete()
            db.session.commit()

            try:
                grade = Grade(
                    student_id=1, 
                    course_id=2, 
                    grade=20, 
                    date_posted=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(grade)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "date_posted" in str(e), "date_posted did not raise an error as expected"

    def test_student_id_must_be_integer(self):
        """Requires student_id to be an integer"""

        with app.app_context():
            Grade.query.delete()
            db.session.commit

            try:

                grade = Grade(
                    student_id='one', 
                    course_id=2, 
                    grade=20, 
                    date_posted=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(grade)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "student_id" in str(e), "Non-integer student_id did not raise an error as expected"
    
    def test_course_id_must_be_integer(self):
        """Requires course_id to be an integer"""

        with app.app_context():
            Grade.query.delete()
            db.session.commit

            try:

                grade = Grade(
                    student_id=1, 
                    course_id="two", 
                    grade=20, 
                    date_posted=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(grade)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "course_id" in str(e), "Non-integer course_id did not raise an error as expected"

    def test_grade_must_be_integer(self):
        """Requires grade to be an integer"""

        with app.app_context():
            Grade.query.delete()
            db.session.commit

            try:
                grade = Grade(
                    student_id=1, 
                    course_id=2, 
                    grade='twenty', 
                    date_posted=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(grade)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "grade" in str(e), "Non-integer grade did not raise an error as expected"

    def test_valid_upload_date(self):
        """Requires upload_date to not be in the future"""

        with app.app_context():
            Grade.query.delete()
            db.session.commit()

            future_date = datetime(2050, 9, 1, 10, 0, 0)
            try:
                grade = Grade(
                    student_id=1, 
                    course_id=2, 
                    grade=20, 
                    date_posted=future_date
                )
                db.session.add(grade)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "future_date" in str(e), "future_date did not raise an error as expected"
