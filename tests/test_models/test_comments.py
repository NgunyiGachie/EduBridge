from app import app
from database import db
from application.models.comments import Comment
from datetime import datetime

class TestComments:
    """Test case for Comment model"""

    def test_has_attributes(self):
        """Test comments model has attributes: discussion_id, student_id, instructor_id, content, posted_at, edited_at"""

        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            comment = Comment(
                discussion_id=1,
                student_id=1,
                instructor_id=1,
                content="The discussion was great",
                posted_at=datetime(2024, 7, 16),
                edited_at=datetime(2024, 7, 16)
            )
            db.session.add(comment)
            db.session.commit()

            new_comment = Comment.query.filter(Comment.id).first()
            assert new_comment is not None
            assert new_comment.discussion_id == 1
            assert new_comment.student_id == 1
            assert new_comment.instructor_id == 1
            assert new_comment.content == "The discussion is great"
            assert new_comment.posted_at == datetime(2024, 7, 16)
            assert new_comment.edited_at == datetime(2024, 7, 16)

            db.session.delete(new_comment)
            db.session.commit()

    def test_requires_discussion_id(self):
        """Requires each record to have a discussion id"""

        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            try:
                comment = Comment(
                    student_id=1,
                    instructor_id=1,
                    content="The discussion was great",
                    posted_at=datetime(2024, 7, 16),
                    edited_at=datetime(2024, 7, 16)
                )
                db.session.add(comment)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                assert "discussion_id" in str(e), "discussion_id validation did not raise an error as expected"

    def test_requires_student_id(self):
        """Requires each record to have a student_id"""

        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            try:
                comment = Comment(
                    discussion_id=1,
                    instructor_id=1,
                    content="The discussion was great",
                    posted_at=datetime(2024, 7, 16),
                    edited_at=datetime(2024, 7, 16)
                    )
                db.session.add(comment)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                assert "student_id" in str(e), "student_id validation did not raise an error as expected"

    def test_requires_instructor_id(self):
        """Requires each record to have an instructor_id"""

        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            try:
                comment = Comment(
                    discussion_id=1,
                    student_id=1,
                    content="The discussion was great",
                    posted_at=datetime(2024, 7, 16),
                    edited_at=datetime(2024, 7, 16)
                )
                db.session.add(comment)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                assert "instructor_id" in str(e), "instructor_id validation did not raise an error as expected"

    def test_requires_content(self):
        """Requires each record to have content"""
        
        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            try:
                comment = Comment(
                    discussion_id=1,
                    student_id=1,
                    instructor_id=1,
                    posted_at=datetime(2024, 7, 16),
                    edited_at=datetime(2024, 7, 16)
                )
                db.session.add(comment)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                assert "content" in str(e), "content validation did not raise an error as expected"

    def test_requires_posted_at(self):
        """Requires each record to have posted_at"""

        with app.app_context():
            Comment.session.delete()
            db.session.commit

            try:
                comment = Comment(
                    discussion_id=1,
                    student_id=1,
                    instructor_id=1,
                    content="The discussion was great",
                    edited_at=datetime(2024, 7, 16)
                )
                db.session.add(comment)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                assert "posted_at" in str(e), "posted_at validation did not raise an error as expected"

    def test_requires_edited_at(self):
        """Requires each record to have edited_at"""

        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            try:
                comment = Comment(
                    discussion_id=1,
                    student_id=1,
                    instructor_id=1,
                    content="The discussion was great",
                    posted_at=datetime(2024, 7, 16)
                )
                db.session.add(comment)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                assert "edited_at" in str(e), "edited_at validation did not raise an error as expected"

    def test_discussion_id_must_be_integer(self):
        """Requires discussion_id to be an integer"""

        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            try:
                comment = Comment(
                    discussion_id="one",
                    student_id=1,
                    instructor_id=1,
                    content="The discussion was great",
                    posted_at=datetime(2024, 7, 16),
                    edited_at=datetime(2024, 7, 16)
                )
                db.session.add(comment)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
            assert "discussion_id" in str(e), "Non-integer discussion_id did not raise an error"

    def test_student_id_must_be_integer(self):
        """Requires student_id to be an integer"""

        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            try:
                comment = Comment(
                    discussion_id=1,
                    student_id="one",
                    instructor_id=1,
                    content="The discussion was great",
                    posted_at=datetime(2024, 7, 16),
                    edited_at=datetime(2024, 7, 16)
                )
                db.session.add(comment)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
            assert "student_id" in str(e), "Non-integer student_id did not raise an error"

    def test_instructor_id_must_be_integer(self):
        """Requires instructor_id to be an integer"""

        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            try:
                comment = Comment(
                    discussion_id=1,
                    student_id=1,
                    instructor_id="one",
                    content="The discussion was great",
                    posted_at=datetime(2024, 7, 16),
                    edited_at=datetime(2024, 7, 16)
                )
                db.session.add(comment)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
            assert "instructor_id" in str(e), "Non-integer instructor_id did not raise an error"

    def test_content_must_be_string(self):
        """Requires content to be a string"""

        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            try:
                comment = Comment(
                    discussion_id=1,
                    student_id=1,
                    instructor_id=1,
                    content=1,
                    posted_at=datetime(2024, 7, 16),
                    edited_at=datetime(2024, 7, 16)
                )
                db.session.add(comment)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
            assert "content" in str(e), "Non-string content did not raise an error"

    def test_invalid_dates(self):
        """Rejects future date"""

        with app.app_context():
            Comment.query.delete()
            db.session.commit

            future_date = datetime(2030, 5, 10)
            try:
                comment = Comment(
                    discussion_id=1,
                    student_id=1,
                    instructor_id="one",
                    content="The discussion was great",
                    posted_at=future_date,
                    edited_at=future_date
                )
                db.session.add(comment)
                db.session.commit
            except Exception as e:
                db.session.rollback()
            assert "dates" in str(e), "Future date did not raise an error as expected"

    



                
                