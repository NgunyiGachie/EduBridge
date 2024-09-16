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
    db.drop_all()
    db.create_all()

    students = [
        Student(username='antogachie', first_name='Anthony', last_name='Gachie', email='myemail@gmail.com', profile_picture=''),
        Student(username='ruth', first_name='Ruth', last_name='Gathoni', email='youremail@gmail.com', profile_picture=''),
        Student(username='lizk', first_name='Elizabeth', last_name='Wanjiru', email='her@gmail.com', profile_picture=''),
        Student(username='sylviah', first_name='Sylviah', last_name='Muthoni', email='sis@gmail.com', profile_picture=''),
        Student(username='ken', first_name='Kennedy', last_name='Kamau', email='bro@gmail.com', profile_picture='')
    ]
    
    for student, password in zip(students, ['password1', 'password2', 'password3', 'password4', 'password5']):
        student.password_hash = ph.generate_password_hash(password).decode('utf-8')
    db.session.add_all(students)
    db.session.commit()

    instructors = [
        Instructor(name='Anthony', profile_picture='', department='Chemistry', bio='Professor in Organic Chemistry'),
        Instructor(name='Dr. Gachie', profile_picture='', department='Computer Science', bio='Professor in Python'),
        Instructor(name='Dr. Ngunyi', profile_picture='', department='Arts', bio='Professor of Philosophy'),
    ]

    for instructor, password in zip(instructors, ['password1', 'password2', 'password3']):
        instructor.password_hash = ph.generate_password_hash(password).decode('utf-8')
    db.session.add_all(instructors)
    db.session.commit()

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

    db.session.add_all(courses)
    db.session.commit()

    ##Seed Assignments
    assignments = [
        Assignment(title='Introduction to Philosophy', course_id='1', due_date=datetime.striptime('2024-16-07T00:00:00', '%Y-%m-%dT%H:%M:%S')),
        Assignment(title='Introduction to Biology', course_id='2', due_date=datetime.striptime('2024-16-07T00:00:00', '%Y-%m-%dT%H:%M:%S')),
        Assignment(title='Introduction to Chemistry', course_id='3', due_date=datetime.striptime('2024-16-07T00:00:00', '%Y-%m-%dT%H:%M:%S')),
        Assignment(title='Introduction to Government', course_id='4', due_date=datetime.striptime('2024-16-07T00:00:00', '%Y-%m-%dT%H:%M:%S')),
    ]

    db.session.add_all(assignments)
    db.session.commit()

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
    db.session.add_all(lectures)
    db.session.commit()

    ##Seed attendance
    attendances = [
        Attendance(student_id='1', lecture_id='1', attendance_status='Present', dates=''),
        Attendance(student_id='2', lecture_id='2', attendance_status='Absent', dates=''),
        Attendance(student_id='3', lecture_id='3', attendance_status='absent', dates='')
    ]
    db.session.add_all(attendances)
    db.session.commit

    #Seed Discussions
    discussions = [
        Discussion(title='What is the role of Philosophy', description='Understand philosophy', course_id='1', created_at='', updated_at=''),
        Discussion(title='Discuss the dichotomous key', description='Understand biology', course_id='2', created_at='', updated_at=''),
        Discussion(title='What is radiation', description='Understand radioactivity', course_id='3', created_at='', updated_at=''),
        Discussion(title='The role of social media', description='Understand sociology', course_id='3', created_at='', updated_at=''),
        Discussion(title='What is the role of mathematics', description='Understand mathematics', course_id='2', created_at='', updated_at=''),
    ]
    db.session.add_all(discussions)
    db.session.commit()

    #Seed Comments
    comments = [
        Comment(discussion_id='1', student_id='1', instructor_id='1', content='I loved the topic', posted_at='', edited_at=''),
        Comment(discussion_id='2', student_id='2', instructor_id='1', content='The topic was awesome', posted_at='', edited_at=''),
        Comment(discussion_id='3', student_id='3', instructor_id='1', content='I had some problems', posted_at='', edited_at=''),
        Comment(discussion_id='4', student_id='4', instructor_id='1', content='I loved the class', posted_at='', edited_at=''),
        Comment(discussion_id='2', student_id='2', instructor_id='1', content='Looking forward to more discussions', posted_at='', edited_at=''),
    ]
    db.session.add_all(comments)
    db.session.commit()

    #Seed Enrollments
    enrollments = [
        Enrollment(course_id='1', student_id='1', status='approved'),
        Enrollment(course_id='2', student_id='2', status='pending'),
        Enrollment(course_id='3', student_id='3', status='pending'),
        Enrollment(course_id='3', student_id='2', status='approved'),
        Enrollment(course_id='2', student_id='1', status='approved'),
    ]
    db.session.add_all(enrollments)
    db.session.commit()

    #Seed Grades
    grades = [
        Grade(student_id='1', course_id='2', grade='20', date_posted=''),
        Grade(student_id='2', course_id='1', grade='90', date_posted=''),
        Grade(student_id='3', course_id='3', grade='40', date_posted=''),
        Grade(student_id='4', course_id='2', grade='30', date_posted=''),
        Grade(student_id='1', course_id='1', grade='34', date_posted=''),
    ]
    db.session.add_all(grades)
    db.session.commit()

    #Seed Files
    files = [
        File(file_info='', related_to='', upload_date=''),
        File(file_info='', related_to='', upload_date=''),
        File(file_info='', related_to='', upload_date=''),
        File(file_info='', related_to='', upload_date=''),
        File(file_info='', related_to='', upload_date=''),
    ]
    db.session.add_all(files)
    db.session.commit()

    #Seed Notifications
    notifications = [
        Notification(title='Class is at ten', message_body='Please attend the class', instructor_id='2', read_status='read', sent_date='', read_date=''),
        Notification(title='Postponed', message_body='I will not attend class', instructor_id='1', read_status='unread', sent_date='', read_date=''),
        Notification(title='Assignment', message_body='Please check new assignment', instructor_id='2', read_status='read', sent_date='', read_date=''),
        Notification(title='Deadline extension', message_body='The deadline for assignment has been extended', instructor_id='2', read_status='read', sent_date='', read_date=''),
        Notification(title='Class is at eleven', message_body='Class time has been pushed to eleven', instructor_id='3', read_status='read', sent_date='', read_date='')
    ]
    db.session.add_all(notifications)
    db.session.commit()

    #Seed Submissions
    submissions = [
        Submission(assignment_id='3', student_id='2', submission_info='', grade_id='1', date=''),
        Submission(assignment_id='2', student_id='1', submission_info='', grade_id='2', date=''),
        Submission(assignment_id='1', student_id='3', submission_info='', grade_id='3', date=''),
        Submission(assignment_id='3', student_id='4', submission_info='', grade_id='1', date=''),
        Submission(assignment_id='1', student_id='2', submission_info='', grade_id='2', date=''),
    ]
    db.session.add_all(submissions)
    db.session.commit()