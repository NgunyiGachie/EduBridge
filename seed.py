import os
from .database import db
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
from .app import app
from .config import config
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
            username='ruth', 
            first_name='Ruth', 
            last_name='Gathoni', 
            email='youremail@gmail.com', 
            profile_picture='https://example.com/images/ruth.jpg'
            ),
        Student(
            username='lizk', 
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
            username='ken', 
            first_name='Kennedy', 
            last_name='Kamau', 
            email='bro@gmail.com', 
            profile_picture='https://example.com/images/ken.jpg'
            )
    ]
    
    for student, password in zip(students, ['password1', 'password2', 'password3', 'password4', 'password5']):
        student.password_hash = ph.generate_password_hash(password).decode('utf-8')
   
    print("Adding students to the database...")
    db.session.add_all(students)
    db.session.commit()
    print(f"{len(students)} students added.")

    instructors = [
        Instructor(
            name='Anthony', 
            profile_picture='', 
            department='Chemistry', 
            bio='Professor in Organic Chemistry'
            ),
        Instructor(
            name='Dr. Gachie', 
            profile_picture='', 
            department='Computer Science', 
            bio='Professor in Python'
            ),
        Instructor(
            name='Dr. Ngunyi', 
            profile_picture='', 
            department='Arts', 
            bio='Professor of Philosophy'
            ),
    ]

    for instructor, password in zip(instructors, ['password1', 'password2', 'password3']):
        instructor.password_hash = ph.generate_password_hash(password).decode('utf-8')
    
    print("Adding instructors to the database...")
    db.session.add_all(instructors)
    db.session.commit()
    print(f"{len(instructors)} courses added.")

    ##Seed Courses
    courses = [
        Course(course_info="Biology for dummies", instructor_id='1', schedule={
            "Monday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Wednesday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Friday": {"start": "09:00 AM", "end": "10:30 AM"}
        }),
        Course(course_info='Ancient Philosophy', instructor_id='2', schedule={
            "Monday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Wednesday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Friday": {"start": "09:00 AM", "end": "10:30 AM"}
        }),
        Course(course_info='Chemistry for dummies', instructor_id='3', schedule={
            "Monday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Wednesday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Friday": {"start": "09:00 AM", "end": "10:30 AM"}
        }),
        Course(course_info='Goverment and History', instructor_id='3', schedule={
            "Monday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Wednesday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Friday": {"start": "09:00 AM", "end": "10:30 AM"}
        }),
    ]
    
    print("Adding courses to the database...")
    db.session.add_all(courses)
    db.session.commit()
    print(f"{len(courses)} courses added.")

    ##Seed Assignments
    assignments = [
        Assignment(
            title='Introduction to Philosophy', 
            course_id='1', 
            due_date=datetime.striptime('2024-16-07T00:00:00', '%Y-%m-%dT%H:%M:%S')
            ),
        Assignment(
            title='Introduction to Biology', 
            course_id='2', 
            due_date=datetime.striptime('2024-16-07T00:00:00', '%Y-%m-%dT%H:%M:%S')
            ),
        Assignment(
            title='Introduction to Chemistry', 
            course_id='3', 
            due_date=datetime.striptime('2024-16-07T00:00:00', '%Y-%m-%dT%H:%M:%S')
            ),
        Assignment(
            title='Introduction to Government', 
            course_id='4', 
            due_date=datetime.striptime('2024-16-07T00:00:00', '%Y-%m-%dT%H:%M:%S')
            ),
    ]
    
    print("Adding assignments to the database...")
    db.session.add_all(assignments)
    db.session.commit()
    print(f"{len(assignments)} assignments added.")

    #Seed Lectures
    lectures = [
        Lecture(instructor_id='1', schedule={
            "Monday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Wednesday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Friday": {"start": "09:00 AM", "end": "10:30 AM"}
        }, created_at='', updated_at=''),
        Lecture(instructor_id='2', schedule={
            "Monday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Wednesday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Friday": {"start": "09:00 AM", "end": "10:30 AM"}
        }, created_at='', updated_at=''),
        Lecture(instructor_id='3', schedule={
            "Monday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Wednesday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Friday": {"start": "09:00 AM", "end": "10:30 AM"}
        }, created_at='', updated_at=''),
        Lecture(instructor_id='4', schedule={
            "Monday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Wednesday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Friday": {"start": "09:00 AM", "end": "10:30 AM"}
        }, created_at='', updated_at=''),
        Lecture(instructor_id='5', schedule={
            "Monday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Wednesday": {"start": "09:00 AM", "end": "10:30 AM"},
            "Friday": {"start": "09:00 AM", "end": "10:30 AM"}
        }, created_at='', updated_at=''),
    ]
    
    print("Adding lectures to the database...")
    db.session.add_all(lectures)
    db.session.commit()
    print(f"{len(lectures)} lectures added.")

    ##Seed attendance
    attendances = [
        Attendance(
            student_id='1', 
            lecture_id='1', 
            attendance_status='Present', 
            dates=datetime.striptime('2024-16-07T00:00:00', '%Y-%m-%dT%H:%M:%S')
            ),
        Attendance(
            student_id='2', 
            lecture_id='2', 
            attendance_status='Absent', 
            dates=datetime.striptime('2024-16-07T00:00:00', '%Y-%m-%dT%H:%M:%S')
            ),
        Attendance(
            student_id='3', 
            lecture_id='3', 
            attendance_status='absent', 
            dates=datetime.striptime('2024-16-07T00:00:00', '%Y-%m-%dT%H:%M:%S')
            )
    ]
    
    
    print("Adding attendances to the database...")
    db.session.add_all(attendances)
    db.session.commit
    print(f"{len(attendances)} attendances added.")

    #Seed Discussions
    discussions = [
        Discussion(
            title='What is the role of Philosophy', 
            description='Understand philosophy', 
            course_id='1', 
            created_at=datetime(2024, 9, 1, 10, 0, 0), 
            updated_at=datetime(2024, 9, 1, 10, 0, 0),
            ),
        Discussion(
            title='Discuss the dichotomous key', 
            description='Understand biology', 
            course_id='2', 
            created_at=datetime(2024, 9, 1, 10, 0, 0), 
            updated_at=datetime(2024, 9, 1, 10, 0, 0),
            ),
        Discussion(
            title='What is radiation', 
            description='Understand radioactivity', 
            course_id='3', 
            created_at=datetime(2024, 9, 1, 10, 0, 0), 
            updated_at=datetime(2024, 9, 1, 10, 0, 0),
            ),
        Discussion(
            title='The role of social media', 
            description='Understand sociology', 
            course_id='3', 
            created_at=datetime(2024, 9, 1, 10, 0, 0), 
            updated_at=datetime(2024, 9, 1, 10, 0, 0),
            ),
        Discussion(
            title='What is the role of mathematics', 
            description='Understand mathematics', 
            course_id='2', 
            created_at=datetime(2024, 9, 1, 10, 0, 0), 
            updated_at=datetime(2024, 9, 1, 10, 0, 0),
            ),
    ]
    
    
    print("Adding discussions to the database...")
    db.session.add_all(discussions)
    db.session.commit()
    print(f"{len(discussions)} discussions added.")

    #Seed Comments
    comments = [
        Comment(
            discussion_id='1', 
            student_id='1', 
            instructor_id='1', 
            content='I loved the topic', 
            posted_at=datetime(2024, 9, 1, 10, 0, 0), 
            edited_at=datetime(2024, 9, 1, 10, 0, 0),
            ),
        Comment(
            discussion_id='2', 
            student_id='2', 
            instructor_id='1', 
            content='The topic was awesome', 
            posted_at=datetime(2024, 9, 1, 10, 0, 0), 
            edited_at=datetime(2024, 9, 1, 10, 0, 0)
            ),
        Comment(
            discussion_id='3', 
            student_id='3', 
            instructor_id='1', 
            content='I had some problems', 
            posted_at=datetime(2024, 9, 1, 10, 0, 0), 
            edited_at=datetime(2024, 9, 1, 10, 0, 0),
            ),
        Comment(
            discussion_id='4', 
            student_id='4', 
            instructor_id='1', 
            content='I loved the class', 
            posted_at=datetime(2024, 9, 1, 10, 0, 0), 
            edited_at=datetime(2024, 9, 1, 10, 0, 0),
            ),
        Comment(
            discussion_id='2', 
            student_id='2', 
            instructor_id='1', 
            content='Looking forward to more discussions', 
            posted_at=datetime(2024, 9, 1, 10, 0, 0), 
            edited_at=datetime(2024, 9, 1, 10, 0, 0)
            ),
    ]
    
    
    print("Adding comments to the database...")
    db.session.add_all(comments)
    db.session.commit()
    print(f"{len(comments)} comments added.")

    #Seed Enrollments
    enrollments = [
        Enrollment(course_id='1', student_id='1', status='approved'),
        Enrollment(course_id='2', student_id='2', status='pending'),
        Enrollment(course_id='3', student_id='3', status='pending'),
        Enrollment(course_id='3', student_id='2', status='approved'),
        Enrollment(course_id='2', student_id='1', status='approved'),
    ]
    
    
    print("Adding enrollments to the database...")
    db.session.add_all(enrollments)
    db.session.commit()
    print(f"{len(enrollments)} enrollments added.")

    #Seed Grades
    grades = [
        Grade(student_id='1', course_id='2', grade='20', date_posted=datetime(2024, 9, 1, 10, 0, 0)),
        Grade(student_id='2', course_id='1', grade='90', date_posted=datetime(2024, 9, 1, 10, 0, 0)),
        Grade(student_id='3', course_id='3', grade='40', date_posted=datetime(2024, 9, 1, 10, 0, 0)),
        Grade(student_id='4', course_id='2', grade='30', date_posted=datetime(2024, 9, 1, 10, 0, 0)),
        Grade(student_id='1', course_id='1', grade='34', date_posted=datetime(2024, 9, 1, 10, 0, 0)),
    ]
    
    
    print("Adding grades to the database...")
    db.session.add_all(grades)
    db.session.commit()
    print(f"{len(grades)} grades added.")

    #Seed Files
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
    
    
    print("Adding students to the database...")
    db.session.add_all(files)
    db.session.commit()
    print(f"{len(grades)} grades added.")

    #Seed Notifications
    notifications = [
        Notification(
            title='Class is at ten', 
            message_body='Please attend the class', 
            instructor_id='2', 
            read_status='read', 
            sent_date=datetime(2024, 9, 1, 9, 0, 0), 
            read_date=datetime(2024, 9, 1, 9, 0, 0),
            ),
        Notification(
            title='Postponed', 
            message_body='I will not attend class', 
            instructor_id='1', 
            read_status='unread', 
            sent_date=datetime(2024, 9, 1, 9, 0, 0), 
            read_date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Notification(
            title='Assignment', 
            message_body='Please check new assignment', 
            instructor_id='2', 
            read_status='read', 
            sent_date=datetime(2024, 9, 1, 9, 0, 0), 
            read_date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Notification(
            title='Deadline extension', 
            message_body='The deadline for assignment has been extended', 
            instructor_id='2', 
            read_status='read', 
            sent_date=datetime(2024, 9, 1, 9, 0, 0), 
            read_date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Notification(
            title='Class is at eleven', 
            message_body='Class time has been pushed to eleven', 
            instructor_id='3', 
            read_status='read', 
            sent_date=datetime(2024, 9, 1, 9, 0, 0), 
            read_date=datetime(2024, 9, 1, 9, 0, 0)
            )
    ]
    
    
    print("Adding notifications to the database...")
    db.session.add_all(notifications)
    db.session.commit()
    print(f"{len(notifications)} notifications added.")

    #Seed Submissions
    submissions = [
        Submission(
            assignment_id='3', 
            student_id='2', 
            submission_info='Assignment 3 submission - Chemistry lab report.pdf', 
            grade_id='1', 
            date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Submission(
            assignment_id='2', 
            student_id='1', 
            submission_info='Assignment 2 submission - Philosophy essay.docx', 
            grade_id='2', 
            date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Submission(
            assignment_id='1', 
            student_id='3', 
            submission_info='Assignment 1 submission - Mathematics homework.pdf', 
            grade_id='3', 
            date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Submission(
            assignment_id='3', 
            student_id='4', 
            submission_info='Assignment 3 submission - Chemistry presentation.pptx', 
            grade_id='1', 
            date=datetime(2024, 9, 1, 9, 0, 0)
            ),
        Submission(
            assignment_id='1', 
            student_id='2', 
            submission_info='Assignment 1 submission - Mathematics quiz.pdf', 
            grade_id='2', 
            date=datetime(2024, 9, 1, 9, 0, 0)
            ),
    ]
    
    
    print("Adding submissions to the database...")
    db.session.add_all(submissions)
    db.session.commit()
    print(f"{len(submissions)} submissions added.")