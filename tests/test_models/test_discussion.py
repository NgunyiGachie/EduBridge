from app import app
from database import db
from application.models.discussion import Discussion
from datetime import datetime

class TestDiscussion:
    """Test case for Discussion model"""

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

            try:
                discussion = Discussion (
                    description='Understand philosophy', 
                    course_id=1, 
                    created_at=datetime(2024, 9, 1, 10, 0, 0), 
                    updated_at=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(discussion)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "title" in str(e), "title validation did not raise an error as expected"

    def test_requires_description(self):
        """Requires each record to have description"""

        with app.app_context():
            Discussion.query.delete()
            db.session.commit()

            try:
                discussion = Discussion(
                    title='What is the role of Philosophy?', 
                    course_id=1, 
                    created_at=datetime(2024, 9, 1, 10, 0, 0), 
                    updated_at=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(discussion)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "description" in str(e), "description validation did not raise an error as expected"

    def test_requires_course_id(self):
        """Requires each test to have a course_id"""
        
        with app.app_context():
            Discussion.query.delete()
            db.session.commit()

            try:
                discussion = Discussion (
                    title='What is the role of Philosophy?', 
                    description='Understand philosophy', 
                    created_at=datetime(2024, 9, 1, 10, 0, 0), 
                    updated_at=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(discussion)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "course_id" in str(e), "course_id validation did not raise an error as expected"

    def test_requires_created_at(self):
        """Requires each record to have created_at"""

        with app.app_context():
            Discussion.query.delete()
            db.session.commit()

            try:
                discussion = Discussion(
                    title='What is the role of Philosophy?', 
                    description='Understand philosophy', 
                    course_id=1,  
                    updated_at=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(discussion)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "created_at" in str(e), "created_at validation did not raise an error as expected"

    def test_requires_updated_at(self):
        """Requires each record to have updated_at"""

        with app.app_context():
            Discussion.query.delete()
            db.session.commit()

            try:
                discussion = Discussion(
                    title='What is the role of Philosophy?', 
                    description='Understand philosophy', 
                    course_id=1, 
                    created_at=datetime(2024, 9, 1, 10, 0, 0), 
                )
                db.session.add(discussion)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "updated_at" in str(e), "updated_at validation did not raise an error as expected"

    def test_title_must_be_string(self):
        """Requires title to be a string"""

        with app.app_context():
            Discussion.query.delete()
            db.session.commit()

            try:
                discussion = Discussion(
                    title=1, 
                    description='Understand philosophy', 
                    course_id=1, 
                    created_at=datetime(2024, 9, 1, 10, 0, 0), 
                    updated_at=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(discussion)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "title" in str(e), "Non-string title did not raise an error as expected"

    def test_description_must_be_string(self):
        """Requires description to be a string"""

        with app.app_context():
            Discussion.query.delete()
            db.session.commit()

            try:
                discussion = Discussion(
                    title='What is the role of Philosophy?', 
                    description=1, 
                    course_id=1, 
                    created_at=datetime(2024, 9, 1, 10, 0, 0), 
                    updated_at=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(discussion)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "description" in str(e), "Non-string description did not raise an error as expected"

    def test_course_id_must_be_integer(self):
        """Requires course_id to be an integer"""

        with app.app_context():
            Discussion.query.delete()
            db.session.commit()

            try:
                discussion = Discussion(
                    title='What is the role of Philosophy?', 
                    description='Understand philosophy', 
                    course_id="one", 
                    created_at=datetime(2024, 9, 1, 10, 0, 0), 
                    updated_at=datetime(2024, 9, 1, 10, 0, 0)
                )
                db.session.add(discussion)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "course_id" in str(e), "Non-integer course_id did not raise an error as expected"

    def test_invalid_dates(self):
        """Rejects future date"""

        with app.app_context():
            Discussion.query.delete()
            db.session.commit

            future_date = datetime(2030, 5, 10)
            try:
                discussion = Discussion(
                    title='What is the role of Philosophy?', 
                    description='Understand philosophy', 
                    course_id=1, 
                    created_at=future_date, 
                    updated_at=future_date
                )
                db.session.add(discussion)
                db.session.commit
            except Exception as e:
                db.session.rollback()
            assert "dates" in str(e), "Future date did not raise an error as expected"

    
     