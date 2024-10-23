"""
students_resource.py - Flask Resource for managing students.
"""

from flask import jsonify, request, make_response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from database import db
from application.models.students import Student

class StudentResource(Resource):
    """Resource for managing student data."""

    def get(self):
        """
        Get all students
        ---
        responses:
            200:
                description: A list of students
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/Student'
            500:
                description: Internal Server Error
        """
        try:
            students = Student.query.all()
            return jsonify([student.to_dict() for student in students])
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server Error"}, 500

    def post(self):
        """
        Create new student
        ---
        parameters:
            - in: formData
              name: username
              type: string
              required: true
              description: Student username
            - in: formData
              name: first_name
              type: string
              required: true
              description: Student first name
            - in: formData
              name: last_name
              type: string
              required: true
              description: Student last name
            - in: formData
              name: email
              type: string
              required: true
              description: Student email
            - in: formData
              name: _password_hash
              type: string
              required: true
              description: Student password
            - in: formData
              name: profile_picture
              type: string
              required: true
              description: Student profile picture
        responses:
            201:
                description: Student successfully created
            400:
                description: Missing required field
            500:
                description: Internal server error
        """
        try:
            new_student = Student(
                username=request.form['username'],
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                _password_hash=request.form['_password_hash'],
                profile_picture=request.form['profile_picture'],
            )
            db.session.add(new_student)
            db.session.commit()
            response_dict = new_student.to_dict()
            return make_response(jsonify(response_dict), 201)
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(
                jsonify({"error": f"Missing required field: {ke}"}), 400
            )
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating student: {e}")
            return make_response(
                jsonify({"error": "Unable to create student", "details": str(e)}),
                500
            )

class StudentByID(Resource):
    """Resource for managing a student by ID."""

    def get(self, student_id):
        """
        Get student by ID
        ---
        parameters:
            - in: path
              name: student_id
              type: integer
              required: true
              description: The ID of the student to retrieve
        responses:
            200:
                description: Student data
            404:
                description: Student not found
        """
        student = Student.query.filter_by(id=student_id).first()
        if student is None:
            return make_response(jsonify({"error": "Student not found"}), 404)
        return make_response(jsonify(student.to_dict()), 200)

    def patch(self, student_id):
        """
        Update student by ID
        ---
        parameters:
            - in: path
              name: student_id
              type: integer
              required: true
              description: The ID of the student to update
            - in: body
              name: body
              schema:
                  $ref: '#/definitions/Student'
        responses:
            200:
                description: Student successfully updated
            400:
                description: Invalid data or student not found
        """
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return make_response(jsonify({"error": "Student not found"}), 404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data"}), 400)

        for attr, value in data.items():
            if hasattr(student, attr):
                setattr(student, attr, value)

        try:
            db.session.commit()
            return make_response(jsonify(student.to_dict()), 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(
                jsonify({"error": "Unable to update student", "details": str(e)}),
                500
            )

    def delete(self, student_id):
        """
        Delete student by ID
        ---
        parameters:
            - in: path
              name: student_id
              type: integer
              required: true
              description: The ID of the student to delete
        responses:
            200:
                description: Student successfully deleted
            404:
                description: Student not found
        """
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return make_response(jsonify({"error": "Student not found"}), 404)

        try:
            db.session.delete(student)
            db.session.commit()
            return make_response({"message": "Student successfully deleted"}, 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(
                jsonify({"error": "Unable to delete student", "details": str(e)}),
                500
            )
