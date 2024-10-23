"""
This module serves as the entry point for the Flask application.
It initializes the app, sets up configurations, and registers routes.
"""

import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flasgger import Swagger
from database import db
from config import config
from application.resources.assignmentResource import AssignmentResource, AssignmentByID
from application.resources.attendanceResource import AttendanceResource, AttendanceByID
from application.resources.commentsResource import CommentResource, CommentByID
from application.resources.courseResource import CourseResource, CourseByID
from application.resources.discussionResource import DiscussionResource, DiscussionByID
from application.resources.enrollmentsResource import EnrollmentsResource, EnrollmentByID
from application.resources.filesResource import FilesResource, FileByID
from application.resources.gradesResource import GradesResource, GradeByID
from application.resources.instructorsResource import InstructorResource, InstructorByID
from application.resources.lecturesResource import LecturesResource, LectureByID
from application.resources.notificationsResource import NotificationsResource, NotificationByID
from application.resources.studentsResource import StudentResource, StudentByID
from application.resources.submissionResource import SubmissionResource, SubmissionByID

app = Flask(__name__)
swagger = Swagger(app)

config_name = os.getenv("FLASK_CONFIG", "default")
app.config.from_object(config[config_name])

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Registering resources
api.add_resource(AssignmentResource, "/assignments", endpoint="assignments")
api.add_resource(AssignmentByID, "/assignments/<int:id>", endpoint="assignments_by_id")
api.add_resource(AttendanceResource, "/attendances", endpoint="attendances")
api.add_resource(AttendanceByID, "/attendances/<int:id>", endpoint="attendances_by_id")
api.add_resource(CommentResource, "/comments", endpoint="comments")
api.add_resource(CommentByID, "/comments/<int:id>", endpoint="comments_by_id")
api.add_resource(CourseResource, "/courses", endpoint="courses")
api.add_resource(CourseByID, "/courses/<int:id>", endpoint="courses_by_id")
api.add_resource(DiscussionResource, "/discussions", endpoint="discussions")
api.add_resource(DiscussionByID, "/discussions/<int:id>", endpoint="discussions_by_id")
api.add_resource(EnrollmentsResource, "/enrollments", endpoint="enrollments")
api.add_resource(EnrollmentByID, "/enrollments/<int:id>", endpoint="enrollments_by_id")
api.add_resource(FilesResource, "/files", endpoint="files")
api.add_resource(FileByID, "/files/<int:id>", endpoint="files_by_id")
api.add_resource(GradesResource, "/grades", endpoint="grades")
api.add_resource(GradeByID, "/grades/<int:id>", endpoint="grades_by_id")
api.add_resource(InstructorResource, "/instructors", endpoint="instructors")
api.add_resource(InstructorByID, "/instructors/<int:id>", endpoint="instructors_by_id")
api.add_resource(LecturesResource, "/lectures", endpoint="lectures")
api.add_resource(LectureByID, "/lectures/<int:id>", endpoint="lectures_by_id")
api.add_resource(NotificationsResource, "/notifications", endpoint="notifications")
api.add_resource(NotificationByID, "/notifications/<int:id>", endpoint="notifications_by_id")
api.add_resource(StudentResource, "/students", endpoint="students")
api.add_resource(StudentByID, "/students/<int:id>", endpoint="students_by_id")
api.add_resource(SubmissionResource, "/submissions", endpoint="submissions")
api.add_resource(SubmissionByID, "/submissions/<int:id>", endpoint="submissions_by_id")

if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 5555))
        app.run(host='0.0.0.0', port=port, debug=True)
    except (ValueError, RuntimeError) as e:
        print(f"An error occurred: {e}")
