import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.submission import Submission
from datetime import datetime

class TestSubmission:
    """Test submission model"""

    def test_has_attributes(self):
        """Has attributes assignment_id, student_id, submission_info, grade_id, date"""

        with app.app_context():
            Submission.query.delete()
            db.session.commit()

            submission = Submission(
                assignment_id=3, 
                student_id=2, 
                submission_info='Assignment 3 submission - Chemistry lab report.pdf', 
                grade_id=1, 
                date=datetime(2024, 9, 1, 9, 0, 0)
            )
            db.session.add(submission)
            db.session.commit()

            created_submission = Submission.query.filter(Submission.submission_info == "Assignment 3 submission - Chemistry lab report.pdf").first()
            assert created_submission is not None
            assert created_submission.assignment_id == 3
            assert created_submission.student_id == 2
            assert created_submission.submission_info == "Assignment 3 submission - Chemistry lab report.pdf"
            assert created_submission.grade_id == 1
            assert created_submission.date == datetime(2024, 9, 1, 9, 0, 0)

    def test_requires_assignment_id(self):
        """Requires each record to have assignment_id"""

        with app.app_context():
            Submission.query.delete()
            db.session.commit()

            submission = Submission(
                student_id=2, 
                submission_info='Assignment 3 submission - Chemistry lab report.pdf', 
                grade_id=1, 
                date=datetime(2024, 9, 1, 9, 0, 0)
            )
            with pytest.raises(IntegrityError):
                db.session.add(submission)
                db.session.commit()

    def test_requires_student_id(self):
        """Requires each record to have student_id"""

        with app.app_context():
            Submission.query.delete()
            db.session.commit()

            submission = Submission(
                assignment_id=3, 
                submission_info='Assignment 3 submission - Chemistry lab report.pdf', 
                grade_id=1, 
                date=datetime(2024, 9, 1, 9, 0, 0)
            )
            with pytest.raises(IntegrityError):
                db.session.add(submission)
                db.session.commit()

    def test_requires_submission_info(self):
        """Requires each record to have submission_info"""

        with app.app_context():
            Submission.query.delete()
            db.session.commit()

            submission = Submission(
                student_id=2, 
                assignment_id=3, 
                grade_id=1, 
                date=datetime(2024, 9, 1, 9, 0, 0)
            )
            with pytest.raises(IntegrityError):
                db.session.add(submission)
                db.session.commit()

    def test_requires_grade_id(self):
        """Requires each record to have grade_id"""

        with app.app_context():
            Submission.query.delete()
            db.session.commit()

            submission = Submission(
                student_id=2, 
                assignment_id=3, 
                submission_info='Assignment 3 submission - Chemistry lab report.pdf', 
                date=datetime(2024, 9, 1, 9, 0, 0)
            )
            with pytest.raises(IntegrityError):
                db.session.add(submission)
                db.session.commit()

    def test_requires_date(self):
        """Requires each record to have a date"""

        with app.app_context():
            Submission.query.delete()
            db.session.commit()

            submission = Submission(
                student_id=2, 
                assignment_id=3, 
                submission_info='Assignment 3 submission - Chemistry lab report.pdf', 
                grade_id=1
            )
            with pytest.raises(IntegrityError):
                db.session.add(submission)
                db.session.commit()

            submission_with_date = Submission(
                student_id=2, 
                assignment_id=3, 
                submission_info='Assignment 3 submission - Chemistry lab report.pdf', 
                grade_id=1,
                date=datetime.now() 
            )
            db.session.add(submission_with_date)
            db.session.commit()  

    def test_integer_values(self):
        """Requires assignment_id, student_id, grade_id to be integers"""

        with app.app_context():
            Submission.query.delete()
            db.session.commit()

            submission_with_non_integer_assignment_id = Submission(
                assignment_id="3", 
                student_id=2, 
                submission_info='Assignment 3 submission - Chemistry lab report.pdf', 
                grade_id=1, 
                date=datetime(2024, 9, 1, 9, 0, 0)
            )
            with pytest.raises(ValueError, match="assignment_id must be an integer"):
                db.session.add(submission_with_non_integer_assignment_id)
                db.session.commit()
            
            submission_with_non_integer_student_id = Submission(
                assignment_id=3, 
                student_id='2', 
                submission_info='Assignment 3 submission - Chemistry lab report.pdf', 
                grade_id=1, 
                date=datetime(2024, 9, 1, 9, 0, 0)
            )
            with pytest.raises(ValueError, match="student_id must be an integer"):
                db.session.add(submission_with_non_integer_student_id)
                db.session.commit()
                
            submission_with_non_integer_grade_id = Submission(
                assignment_id=3, 
                student_id=2, 
                submission_info='Assignment 3 submission - Chemistry lab report.pdf', 
                grade_id="1", 
                date=datetime(2024, 9, 1, 9, 0, 0)
            )
            
            with pytest.raises(ValueError, match="grade_id must be an integer"):
                db.session.add(submission_with_non_integer_grade_id)
                db.session.commit()

    def test_submission_info_must_be_string(self):
        """Requires submission_info to be a string"""

        with app.app_context():
            Submission.query.delete()
            db.session.commit()

            submission = Submission(
                assignment_id=3, 
                student_id=2, 
                submission_info=2, 
                grade_id=1, 
                date=datetime(2024, 9, 1, 9, 0, 0)
            )
            with pytest.raises(ValueError, match="submission_info must be a string"):
                db.session.add(submission)
                db.session.commit()

    def test_date_is_not_a_future_date(self):
        """Requires date not to be in the future"""

        with app.app_context():
            Submission.query.delete()
            db.session.commit()

            submission = Submission(
                assignment_id=3, 
                student_id=2, 
                submission_info='Assignment 3 submission - Chemistry lab report.pdf', 
                grade_id=1, 
                date=datetime(2024, 9, 1, 9, 0, 0)
            )
            with pytest.raises(ValueError, match="date cannot be in the future"):
                db.session.add(submission)
                db.session.commit()







