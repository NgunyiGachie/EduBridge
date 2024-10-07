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
        Student(username='antogachie', first_name='Anthony', last_name='Gachie', email='myemail@gmail.com', profile_picture='https://example.com/images/antogachie.jpg'),
        Student(username='ruthgath', first_name='Ruth', last_name='Gathoni', email='youremail@gmail.com', profile_picture='https://example.com/images/ruth.jpg'),
        Student(username='lizwanjiru', first_name='Elizabeth', last_name='Wanjiru', email='her@gmail.com', profile_picture='https://example.com/images/lizk.jpg'),
        Student(username='sylviah', first_name='Sylviah', last_name='Muthoni', email='sis@gmail.com', profile_picture='https://example.com/images/sylviah.jpg'),
        Student(username='kenkamau', first_name='Kennedy', last_name='Kamau', email='bro@gmail.com', profile_picture='https://example.com/images/ken.jpg')
    ]

    for student, password in zip(students, ['password1', 'password2', 'password3', 'password4', 'password5']):
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
            bio='Professor in Organic Chemistry'),
        Instructor(
            name='Dr. Gachie',
            email='instructor2@gmail.com', 
            profile_picture='https://example.com/images/dr.jpg', 
            department='Computer Science', 
            bio='Professor in Python'),
        Instructor(
            name='Dr. Ngunyi',
            email='instructor3@gmail.com', 
            profile_picture='https://example.com/images/dr.jpg', 
            department='Arts', 
            bio='Professor of Philosophy')
    ]

    for instructor, password in zip(instructors, ['password1', 'password2', 'password3']):
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
            total_points=70,
            ),
        Assignment(
            title='Introduction to Biology', 
            description='Prepare a dichotomous key',
            course_id=2, 
            due_date=datetime(2024, 11, 16),
            total_points=50,
            ),
        Assignment(
            title='Introduction to Chemistry',
            description='Write an essay about radioactivity', 
            course_id=3, 
            due_date=datetime(2024, 11, 16),
            total_points=30,
            ),
        Assignment(
            title='Introduction to Government', 
            description='Describe the concept of a social contract',
            course_id=4, 
            due_date=datetime(2024, 11, 16),
            total_points=25,
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
        Attendance(student_id=1, lecture_id=1, instructor_id=2, attendance_status='Present', dates=datetime(2024, 7, 16)),
        Attendance(student_id=2, lecture_id=2, instructor_id=2, attendance_status='Absent', dates=datetime(2024, 7, 16)),
        Attendance(student_id=3, lecture_id=3, instructor_id=2, attendance_status='Absent', dates=datetime(2024, 7, 16))
    ]

    try:
        print("Adding attendances to the database...")
        db.session.add_all(attendances)
        db.session.commit()
        print(f"{len(attendances)} attendances added.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()

    # Seed Discussions
    discussions = [
        Discussion(title='What is the role of Philosophy?', description='Understand philosophy', course_id=1, created_at=datetime(2024, 9, 1, 10, 0, 0), updated_at=datetime(2024, 9, 1, 10, 0, 0)),
        Discussion(title='Discuss the dichotomous key', description='Understand biology', course_id=2, created_at=datetime(2024, 9, 1, 10, 0, 0), updated_at=datetime(2024, 9, 1, 10, 0, 0)),
        Discussion(title='What is radiation?', description='Understand radioactivity', course_id=3, created_at=datetime(2024, 9, 1, 10, 0, 0), updated_at=datetime(2024, 9, 1, 10, 0, 0))
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

    # Seed Comments
    comments = [
        Comment(discussion_id=1, student_id=1, instructor_id=1, content='I loved the topic', posted_at=datetime(2024, 9, 1, 10, 0, 0), edited_at=datetime(2024, 9, 1, 10, 0, 0)),
        Comment(discussion_id=2, student_id=2, instructor_id=1, content='The topic was awesome', posted_at=datetime(2024, 9, 1, 10, 0, 0), edited_at=datetime(2024, 9, 1, 10, 0, 0))
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

    # Seed Enrollments
    enrollments = [
        Enrollment(course_id=1, student_id=1, status='enrolled'),
        Enrollment(course_id=2, student_id=2, status='pending'),
        Enrollment(course_id=3, student_id=3, status='pending'),
        Enrollment(course_id=4, student_id=4, status='enrolled')
    ]

    try:
        print("Adding enrollments to the database...")
        db.session.add_all(enrollments)
        db.session.commit()
        print(f"{len(enrollments)} enrollments added.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()

    # Seed Files
    files = [
        File(
            file_info='Course syllabus for Philosophy.pdf', 
            related_to='1', 
            upload_date=datetime(2024, 9, 1, 9, 0, 0),
            ),
        File(
            file_info='Dichotomous key example.png', 
            related_to='2', 
            upload_date=datetime(2024, 9, 1, 9, 0, 0),
            ),
        File(
            file_info='Radioactivity lecture notes.docx', 
            related_to='1', 
            upload_date=datetime(2024, 9, 1, 9, 0, 0),
            ),
        File(
            file_info='Sociology and Social Media research.pdf', 
            related_to='2', 
            upload_date=datetime(2024, 9, 1, 9, 0, 0),
            ),
        File(
            file_info='Sociology and Social Media research.pdf', 
            related_to='1', 
            upload_date=datetime(2024, 9, 1, 9, 0, 0),
            ),
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

    # Seed Grades
    grades = [
        Grade(
            student_id=1, 
            course_id=2, 
            grade=20, 
            date_posted=datetime(2024, 9, 1, 10, 0, 0)
            ),
        Grade(
            student_id=2, 
            course_id=1, 
            grade=90, 
            date_posted=datetime(2024, 9, 1, 10, 0, 0)
            ),
        Grade(
            student_id=3, 
            course_id=3, 
            grade=40, 
            date_posted=datetime(2024, 9, 1, 10, 0, 0)
            ),
        Grade(
            student_id=4, 
            course_id=2, 
            grade=30, 
            date_posted=datetime(2024, 9, 1, 10, 0, 0)
            ),
        Grade(
            student_id=1, 
            course_id=1, 
            grade=34, 
            date_posted=datetime(2024, 9, 1, 10, 0, 0)
            ),
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

    # Seed Notifications
    notifications = [
        Notification(
            title='Class is at ten', 
            message_body='Please attend the class',
            student_id=3, 
            instructor_id=2, 
            read_status='read', 
            sent_date=datetime(2024, 9, 1, 9, 0, 0), 
            read_date=datetime(2024, 9, 1, 9, 0, 0),
            ),
        Notification(
            title='Postponed', 
            message_body='I will not attend class',
            student_id=3, 
            instructor_id=1, 
            read_status='unread', 
            sent_date=datetime(2024, 9, 1, 9, 0, 0), 
            read_date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Notification(
            title='Assignment', 
            message_body='Please check new assignment', 
            student_id=2,
            instructor_id=2, 
            read_status='read', 
            sent_date=datetime(2024, 9, 1, 9, 0, 0), 
            read_date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Notification(
            title='Deadline extension', 
            message_body='The deadline for assignment has been extended', 
            student_id=3,
            instructor_id=2, 
            read_status='read', 
            sent_date=datetime(2024, 9, 1, 9, 0, 0), 
            read_date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Notification(
            title='Class is at eleven', 
            message_body='Class time has been pushed to eleven',
            student_id=1, 
            instructor_id=3, 
            read_status='read', 
            sent_date=datetime(2024, 9, 1, 9, 0, 0), 
            read_date=datetime(2024, 9, 1, 9, 0, 0)
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

    submissions = [
        Submission(
            assignment_id=3, 
            student_id=2, 
            submission_info='Assignment 3 submission - Chemistry lab report.pdf', 
            grade_id=1, 
            date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Submission(
            assignment_id=2, 
            student_id=1, 
            submission_info='Assignment 2 submission - Philosophy essay.docx', 
            grade_id=2, 
            date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Submission(
            assignment_id=1, 
            student_id=3, 
            submission_info='Assignment 1 submission - Mathematics homework.pdf', 
            grade_id=3, 
            date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Submission(
            assignment_id=3, 
            student_id=4, 
            submission_info='Assignment 3 submission - Chemistry presentation.pptx', 
            grade_id=1, 
            date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Submission(
            assignment_id=1, 
            student_id=2, 
            submission_info='Assignment 1 submission - Mathematics quiz.pdf', 
            grade_id=2, 
            date=datetime(2024, 9, 1, 9, 0, 0)
            ),
    ]

    try:
        db.session.add_all(submissions)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()

    print("Seeding complete!")
