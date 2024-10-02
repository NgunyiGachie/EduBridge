from app import app
from database import db
from application.models.files import File
from datetime import datetime

class TestFiles:
    """Test case for Files model"""

    def test_has_attributes(self):
        """Test files model has attributes: file_info, related_to, upload_date"""

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

            new_file = File.query.filter(File.id).first()
            assert new_file is not None
            assert new_file.file_info == 'Course syllabus for Philosophy.pdf'
            assert new_file.related_to == '1'
            assert new_file.upload_date == datetime(2024, 9, 1, 9, 0, 0)

            db.session.delete(new_file)
            db.session.commit()

    def test_requires_file_info(self):
        """Requires each record to have a file_info"""

        with app.app_context():
            File.query.delete()
            db.session.commit()

            try:
                file = File(
                    related_to='1', 
                    upload_date=datetime(2024, 9, 1, 9, 0, 0)
                )
                db.session.add(file)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "file_info" in str(e), "file_info validation did not raise an error as expected"

    def test_requires_related_to(self):
        """Requires each record to have related_to"""

        with app.app_context():
            File.query.delete()
            db.session.commit()

            try:
                file = File(
                    file_info='Course syllabus for Philosophy.pdf', 
                    upload_date=datetime(2024, 9, 1, 9, 0, 0)
                )
                db.session.add(file)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "related_to" in str(e), "related_to validation did not raise an error as expected"

    def test_requires_upload_date(self):
        """Requires each record to have upload_date"""

        with app.app_context():
            File.query.delete()
            db.session.commit()

            try:
                file = File(
                    file_info='Course syllabus for Philosophy.pdf', 
                    related_to='1'
                )
                db.session.add(file)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "upload_date" in str(e), "upload_date validation did not raise an error as expected"

    def test_file_info_must_be_string(self):
        """Requires file info to be a string"""

        with app.app_context():
            File.query.delete()
            db.session.commit()

            try:
                file = File(
                    file_info=1, 
                    related_to='1', 
                    upload_date=datetime(2024, 9, 1, 9, 0, 0)
                )
                db.session.add(file)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "file_info" in str(e), "Non-string file_info did not raise an error as expected"

    def test_related_to_must_be_string(self):
        """Requires related_to to be a string"""

        with app.app_context():
            File.query.delete()
            db.session.commit()

            try:
                file = File(
                    file_info='Course syllabus for Philosophy.pdf', 
                    related_to=1, 
                    upload_date=datetime(2024, 9, 1, 9, 0, 0)
                )
                db.session.add(file)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "related_to" in str(e), "Non-string related_to did not raise an error as expected"

    def test_valid_date(self):
        """Requires upload_date to not be in the future"""

        with app.app_context():
            File.query.delete()
            db.session.commit()

            future_date=datetime(2040, 9, 1, 9, 0, 0)
            try: 
                file = File(
                    file_info='Course syllabus for Philosophy.pdf', 
                    related_to='1', 
                    upload_date=future_date
                )
                db.session.add(file)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                assert "future_date" in str(e), "future_date did not raise an error as expected"