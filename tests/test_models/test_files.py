"""Test suite for the File model."""

import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app import app
from database import db
from application.models.files import File

class TestFiles:
    """Test case for the File model."""

    @pytest.fixture
    def setup_teardown(self, app):
        """Set up the database for testing and tear it down afterward."""
        with app.app_context():
            db.create_all()
            yield
            db.session.rollback()
            db.drop_all()

    @pytest.mark.usefixtures("setup_teardown")
    def test_has_attributes(self):
        """Test File model has attributes: file_info, related_to, upload_date."""
        with app.app_context():
            File.query.delete()
            db.session.commit()

            file = File(
                file_info='Course syllabus for Philosophy.pdf',
                related_to='1',
                upload_date=datetime(2024, 9, 1, 9, 0, 0)
            )
            db.session.add(file)
            db.session.commit()

            new_file = File.query.first()
            assert new_file is not None
            assert new_file.file_info == 'Course syllabus for Philosophy.pdf'
            assert new_file.related_to == '1'
            assert new_file.upload_date == datetime(2024, 9, 1, 9, 0, 0)

            db.session.delete(new_file)
            db.session.commit()

    @pytest.mark.usefixtures("setup_teardown")
    def test_requires_file_info(self):
        """Test that each record requires a file_info."""
        with app.app_context():
            File.query.delete()
            db.session.commit()

            file = File(
                related_to='1',
                upload_date=datetime(2024, 9, 1, 9, 0, 0)
            )
            with pytest.raises(IntegrityError):
                db.session.add(file)
                db.session.commit()

    @pytest.mark.usefixtures("setup_teardown")
    def test_requires_related_to(self):
        """Test that each record requires related_to."""
        with app.app_context():
            File.query.delete()
            db.session.commit()

            file = File(
                file_info='Course syllabus for Philosophy.pdf',
                upload_date=datetime(2024, 9, 1, 9, 0, 0)
            )
            with pytest.raises(IntegrityError):
                db.session.add(file)
                db.session.commit()

    @pytest.mark.usefixtures("setup_teardown")
    def test_requires_upload_date(self):
        """Test that each record requires an upload_date."""
        with app.app_context():
            File.query.delete()
            db.session.commit()

            file = File(
                file_info='Course syllabus for Philosophy.pdf',
                related_to='1',
            )
            with pytest.raises(IntegrityError):
                db.session.add(file)
                db.session.commit()
