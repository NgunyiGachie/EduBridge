import os
from database import db
from application.models.assignment import Assignment
from application.models.attendance import Attendance
from application.models.comments import Comment
from application.models.course import Course
from application.models.discussion import Discussion
from application.models.enrollments import Enrollment
from application.models.files import File
from application.models.grades import Grade
from application.models.instructors import Instructor
from application.models.lectures import Lecture
from application.models.notifications import Notification
from application.models.students import Student
from application.models.submission import Submission
from app import app
from config import config
from argon2 import PasswordHasher
from datetime import datetime

ph = PasswordHasher()
config_name = os.getenv('FLASK_CONFIG', 'default')
app.config.from_object(config[config_name])

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()

    students = [
        Student(
            username='antogachie',
            first_name='Anthony',
            last_name='Gachie',
            email='myemail@gmail.com',
            profile_picture='https://example.com/images/antogachie.jpg'
        ),
        Student(
            username='ruthgath',
            first_name='Ruth',
            last_name='Gathoni',
            email='youremail@gmail.com',
            profile_picture='https://example.com/images/ruth.jpg'
        ),
        Student(
            username='lizwanjiru',
            first_name='Elizabeth',
            last_name='Wanjiru',
            email='her@gmail.com',
            profile_picture='https://example.com/images/lizk.jpg'
        ),
        Student(
            username='sylviah',
            first_name='Sylviah',
            last_name='Muthoni',
            email='sis@gmail.com',
            profile_picture='https://example.com/images/sylviah.jpg'
        ),
        Student(
            username='kenkamau',
            first_name='Kennedy',
            last_name='Kamau',
            email='bro@gmail.com',
            profile_picture='https://example.com/images/ken.jpg'
        )
    ]

    for student, password in zip(students,
                                  ['password1', 'password2',
                                   'password3', 'password4',
                                   'password5']):
        student.password_hash = ph.hash(password)

    print("Adding students to the database...")
    db.session.add_all(students)
    db.session.commit()
    print(f"{len(students)} students added.")

    instructors = [
        Instructor(
            name='Anthony',
            email='instructor1@gmail.com',
            profile_picture='https://example.com/images/anthony.jpg',
            department='Chemistry',
            bio='Professor in Organic Chemistry'
        ),
        Instructor(
            name='Dr. Gachie',
            email='instructor2@gmail.com',
            profile_picture='https://example.com/images/dr.jpg',
            department='Computer Science',
            bio='Professor in Python'
        ),
        Instructor(
            name='Dr. Ngunyi',
            email='instructor3@gmail.com',
            profile_picture='https://example.com/images/dr.jpg',
            department='Arts',
            bio='Professor of Philosophy'
        )
    ]

    for instructor, password in zip(instructors,
                                     ['password1', 'password2',
                                      'password3']):
        instructor.password_hash = ph.hash(password)

    print("Adding instructors to the database...")
    db.session.add_all(instructors)
    db.session.commit()
    print(f"{len(instructors)} instructors added.")

    # Seed Courses
    courses = [
        Course(
            course_info="Biology for Dummies",
            instructor_id=1,
            schedule=[
                {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
            ]
        ),
        Course(
            course_info='Ancient Philosophy',
            instructor_id=2,
            schedule=[
                {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
            ]
        ),
        Course(
            course_info='Chemistry for Dummies',
            instructor_id=3,
            schedule=[
                {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
            ]
        ),
        Course(
            course_info='Government and History',
            instructor_id=3,
            schedule=[
                {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
            ]
        )
    ]

    try:
        print("Adding courses to the database...")
        db.session.add_all(courses)
        db.session.commit()
        print(f"{len(courses)} courses added.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()

    # Seed Assignments
    assignments = [
        Assignment(
            title='Introduction to Philosophy',
            description='Explain the allegory of the cave',
            course_id=1,
            due_date=datetime(2024, 11, 16),
            total_points=70
        ),
        Assignment(
            title='Introduction to Biology',
            description='Prepare a dichotomous key',
            course_id=2,
            due_date=datetime(2024, 11, 16),
            total_points=50
        ),
        Assignment(
            title='Introduction to Chemistry',
            description='Write an essay about radioactivity',
            course_id=3,
            due_date=datetime(2024, 11, 16),
            total_points=30
        ),
        Assignment(
            title='Introduction to Government',
            description='Describe the concept of a social contract',
            course_id=4,
            due_date=datetime(2024, 11, 16),
            total_points=25
        )
    ]

    try:
        print("Adding assignments to the database...")
        db.session.add_all(assignments)
        db.session.commit()
        print(f"{len(assignments)} assignments added.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()

    # Seed Lectures
    lectures = [
        Lecture(
            lecture_info='ZOOL 102',
            instructor_id=1,
            schedule=[
                {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
            ],
            created_at=datetime(2024, 9, 16),
            updated_at=datetime(2024, 9, 16)
        ),
        Lecture(
            lecture_info='ECON 101',
            instructor_id=2,
            schedule=[
                {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
            ],
            created_at=datetime(2024, 9, 16),
            updated_at=datetime(2024, 9, 16)
        ),
        Lecture(
            lecture_info='ENG 202',
            instructor_id=3,
            schedule=[
                {"day": "Monday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Wednesday", "start": "09:00 AM", "end": "10:30 AM"},
                {"day": "Friday", "start": "09:00 AM", "end": "10:30 AM"}
            ],
            created_at=datetime(2024, 9, 16),
            updated_at=datetime(2024, 9, 16)
        )
    ]

    try:
        print("Adding lectures to the database...")
        db.session.add_all(lectures)
        db.session.commit()
        print(f"{len(lectures)} lectures added.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()

    # Seed Attendance
    attendances = [
        Attendance(
            student_id=1,
            lecture_id=1,
            instructor_id=2,
            status='present',
            created_at=datetime(2024, 10, 18)
        ),
        Attendance(
            student_id=2,
            lecture_id=2,
            instructor_id=3,
            status='absent',
            created_at=datetime(2024, 10, 18)
        ),
        Attendance(
            student_id=3,
            lecture_id=3,
            instructor_id=2,
            status='present',
            created_at=datetime(2024, 10, 18)
        )
    ]

    try:
        print("Adding attendance records to the database...")
        db.session.add_all(attendances)
        db.session.commit()
        print(f"{len(attendances)} attendance records added.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()

    # Seed Grades
    grades = [
        Grade(
            student_id=1,
            assignment_id=1,
            points_earned=50,
            total_points=70,
            created_at=datetime(2024, 10, 18)
        ),
        Grade(
            student_id=2,
            assignment_id=2,
            points_earned=40,
            total_points=50,
            created_at=datetime(2024, 10, 18)
        ),
        Grade(
            student_id=3,
            assignment_id=3,
            points_earned=25,
            total_points=30,
            created_at=datetime(2024, 10, 18)
        )
    ]

    try:
        print("Adding grades to the database...")
        db.session.add_all(grades)
        db.session.commit()
        print(f"{len(grades)} grades added.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()

    # Seed Files
    files = [
        File(
            filename='assignment1.pdf',
            assignment_id=1,
            file_url='https://example.com/files/assignment1.pdf',
            uploaded_at=datetime(2024, 10, 18)
        ),
        File(
            filename='assignment2.pdf',
            assignment_id=2,
            file_url='https://example.com/files/assignment2.pdf',
            uploaded_at=datetime(2024, 10, 18)
        )
    ]

    try:
        print("Adding files to the database...")
        db.session.add_all(files)
        db.session.commit()
        print(f"{len(files)} files added.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()

    # Seed Discussions
    discussions = [
        Discussion(
            topic='Philosophy of Mind',
            description='Discuss the nature of consciousness',
            course_id=1,
            created_at=datetime(2024, 10, 18)
        ),
        Discussion(
            topic='Biological Classification',
            description='How do we classify living organisms?',
            course_id=2,
            created_at=datetime(2024, 10, 18)
        )
    ]

    try:
        print("Adding discussions to the database...")
        db.session.add_all(discussions)
        db.session.commit()
        print(f"{len(discussions)} discussions added.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()

    # Seed Notifications
    notifications = [
        Notification(
            user_id=1,
            message='Your assignment is due soon.',
            created_at=datetime(2024, 10, 18)
        ),
        Notification(
            user_id=2,
            message='Your attendance has been recorded.',
            created_at=datetime(2024, 10, 18)
        ),
        Notification(
            user_id=3,
            message='New lecture materials are available.',
            created_at=datetime(2024, 10, 18)
        )
    ]

    try:
        print("Adding notifications to the database...")
        db.session.add_all(notifications)
        db.session.commit()
        print(f"{len(notifications)} notifications added.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()

    # Seed Comments
    comments = [
        Comment(
            user_id=1,
            discussion_id=1,
            content='This is a fascinating topic!',
            created_at=datetime(2024, 10, 18)
        ),
        Comment(
            user_id=2,
            discussion_id=2,
            content='I agree, we should classify organisms more accurately.',
            created_at=datetime(2024, 10, 18)
        )
    ]

    try:
        print("Adding comments to the database...")
        db.session.add_all(comments)
        db.session.commit()
        print(f"{len(comments)} comments added.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()

    print("Seeding completed successfully.")
