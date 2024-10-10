import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from database import db
from application.models.discussion import Discussion
from datetime import datetime

class TestDiscussion:
    """Test case for Discussion model"""

    @pytest.fixture
    def setup_teardown(app):
        with app.app_context():
            db.create_all()
            yield
            db.session.rollback()
            db.drop_all()

    def test_has_attributes(self):
        """Test discussion model has attributes: title, description, course_id, created_at, updated_at"""
        with app.app_context():
            Discussion.query.delete()
            db.session.commit

            discussion = Discussion(
                title='What is the role of Philosophy?', 
                description='Understand philosophy', 
                course_id=1, 
                created_at=datetime(2024, 9, 1, 10, 0, 0), 
                updated_at=datetime(2024, 9, 1, 10, 0, 0)
                )
            db.session.add(discussion)
            db.session.commit()

            new_discussion = Discussion.query.filter(Discussion.id).first()
            assert new_discussion is not None
            assert new_discussion.title == 'What is the role of Philosophy?'
            assert new_discussion.description == 'Understand philosophy'
            assert new_discussion.created_at == datetime(2024, 9, 1, 10, 0, 0)
            assert new_discussion.updated_at == datetime(2024, 9, 1, 10, 0, 0)

            db.session.delete(new_discussion)
            db.session.commit()

    def test_requires_title(self):
        """Requires each record to have a title"""

        with app.app_context():
            Discussion.query.delete()
            db.session.commit()

            discussion = Discussion( 
                description='Understand philosophy', 
                course_id=1, 
                created_at=datetime(2024, 9, 1, 10, 0, 0), 
                updated_at=datetime(2024, 9, 1, 10, 0, 0)
                )
            with pytest.raises(IntegrityError):
                db.session.add(discussion)
                db.session.commit()

    def test_requires_description(self):
        """Requires each record to have description"""
        with app.app_context():
            Discussion.query.delete()
            db.session.commit()

            discussion = Discussion(
                title='What is the role of Philosophy?', 
                course_id=1, 
                created_at=datetime(2024, 9, 1, 10, 0, 0), 
                updated_at=datetime(2024, 9, 1, 10, 0, 0)
                )
            with pytest.raises(IntegrityError):
                db.session.add(discussion)
                db.session.commit()

    def test_requires_course_id(self):
        """Requires each test to have a course_id"""
        with app.app_context():
            Discussion.query.delete()
            db.session.commit()

            discussion = Discussion(
                title='What is the role of Philosophy?', 
                description='Understand philosophy',  
                created_at=datetime(2024, 9, 1, 10, 0, 0), 
                updated_at=datetime(2024, 9, 1, 10, 0, 0)
                )
            with pytest.raises(IntegrityError):
                db.session.add(discussion)
                db.session.commit()

    def test_requires_created_at(self):
        """Requires each record to have created_at"""
        with app.app_context():
            Discussion.query.delete()
            db.session.commit()

            discussion = Discussion(
                title='What is the role of Philosophy?', 
                description='Understand philosophy', 
                course_id=1, 
                updated_at=datetime(2024, 9, 1, 10, 0, 0)
                )
            with pytest.raises(IntegrityError):
                db.session.add(discussion)
                db.session.commit()

    def test_requires_updated_at(self):
        """Requires each record to have updated_at"""
        with app.app_context():
            Discussion.query.delete()
            db.session.commit()

            discussion = Discussion(
                title='What is the role of Philosophy?', 
                description='Understand philosophy', 
                course_id=1, 
                created_at=datetime(2024, 9, 1, 10, 0, 0), 
                )
            with pytest.raises(IntegrityError):
                db.session.add(discussion)
                db.session.commit()

    