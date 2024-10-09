import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.comments import Comment
from datetime import datetime

class TestComments:
    """Test case for Comment model"""
    @pytest.fixture
    def setup_teardown(app):
        with app.app_context():
            db.create_all()
            yield
            db.session.rollback()
            db.drop_all()

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
            assert new_comment.content == "The discussion was great"
            assert new_comment.posted_at == datetime(2024, 7, 16)
            assert new_comment.edited_at == datetime(2024, 7, 16)
            assert new_comment.id is not None

            db.session.delete(new_comment)
            db.session.commit()

    def test_requires_discussion_id(self):
        """Requires each record to have a discussion id"""
        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            comment = Comment(
                student_id=1,
                instructor_id=1,
                content="The discussion was great",
                posted_at=datetime(2024, 7, 16),
                edited_at=datetime(2024, 7, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(comment)
                db.session.commit()


    def test_requires_student_id(self):
        """Requires each record to have a student_id"""
        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            comment = Comment(
                discussion_id=1,
                instructor_id=1,
                content="The discussion was great",
                posted_at=datetime(2024, 7, 16),
                edited_at=datetime(2024, 7, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(comment)
                db.session.commit()

    def test_requires_instructor_id(self):
        """Requires each record to have an instructor_id"""
        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            comment = Comment(
                discussion_id=1,
                student_id=1,
                content="The discussion was great",
                posted_at=datetime(2024, 7, 16),
                edited_at=datetime(2024, 7, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(comment)
                db.session.commit()

    def test_requires_content(self):
        """Requires each record to have content"""
        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            comment = Comment(
                discussion_id=1,
                student_id=1,
                instructor_id=1,
                posted_at=datetime(2024, 7, 16),
                edited_at=datetime(2024, 7, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(comment)
                db.session.commit()

    def test_requires_posted_at(self):
        """Requires each record to have posted_at"""
        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            comment = Comment(
                discussion_id=1,
                student_id=1,
                instructor_id=1,
                content="The discussion was great",
                edited_at=datetime(2024, 7, 16)
            )
            with pytest.raises(IntegrityError):
                db.session.add(comment)
                db.session.commit()

    def test_requires_edited_at(self):
        """Requires each record to have edited_at"""
        with app.app_context():
            Comment.query.delete()
            db.session.commit()

            comment = Comment(
                discussion_id=1,
                student_id=1,
                instructor_id=1,
                content="The discussion was great",
                posted_at=datetime(2024, 7, 16),
            )
            with pytest.raises(IntegrityError):
                db.session.add(comment)
                db.session.commit()


   