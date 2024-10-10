import os
from flask import Flask
from flasgger import Swagger
from flask_migrate import Migrate
from database import db
from config import config
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

app = Flask(__name__)
swagger = Swagger(app)

config_name = os.getenv("FLASK_CONFIG", "default")
app.config.from_object(config[config_name])

db.init_app(app)
migrate = Migrate(app, db)

if __name__== '__main__':
    try:
        port = int(os.environ.get("PORT", 5555))
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")