# EduBridge

## Description
EduBridge is an online classroom management system designed to facilitate effective communication and management of educational resources between students and instructors. The application provides a platform for managing student and instructor registrations, assignments, lectures, discussions, comments, courses, enrollments, submissions, notifications, grades, and files.

## Features
- **User Registration**: Both students and instructors can register and create profiles.
- **Course Management**: Instructors can create and manage courses, including lectures and assignments.
- **Assignment Management**: Students can submit assignments, and instructors can grade them.
- **Discussion Forum**: A space for students and instructors to engage in discussions.
- **Notifications**: Real-time notifications for assignments, grades, and announcements.
- **Grade Tracking**: Students can view their grades and feedback on assignments.
- **File Management**: Upload and manage files related to courses and assignments.

## Technologies Used
- **Backend**: Flask
- **Database**: SQLAlchemy (with SQLite for development and PostgreSQL for production)
- **Authentication**: Argon2 for secure password hashing

## Getting Started

### Prerequisites
- Python 3.6 or higher
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Argon2-Cffi
- SQLite or PostgreSQL

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/edubridge.git
   cd edubridge

2. **Set up a virtual environment:**
    ```python -m venv venv
    source venv/bin/activate 

3. **Install dependencies:**
    ```pip install -r requirements.txt

4. **Set up the database:**
    Modify the ```config.py file to configure your database connection.
    Initialize the database:
        ```bash
        python
        from app import db
        db.create_all()
5. **Seed the database:**
    ```python seed.py

### Running the Application
```python app.py`
Open your browser and navigate to http://127.0.0.1:5555/ to access the application.

### Contributing
Contributions are welcome! If you have suggestions for improvements or would like to add new features, please fork the repository and submit a pull request.

### Acknowledgements
    - Inspired by various online classroom management systems.
    - Thanks to the contributors of Flask and SQLAlchemy for their frameworks.




