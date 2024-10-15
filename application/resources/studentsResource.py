from database import db
from application.models.students import Student
from flask import jsonify, request, make_response
from flask_restful import Resource

class StudentResource(Resource):
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
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server Error"}, 500
    
    def post(self):
        """
        create new student
        ---
        parameters:
            -in: formData
            name: username
            type: string
            required: true
            description: Student username
            -in: formData
            name: first_name
            type: string
            required: true
            description: Student first name
            -in: formData
            name: last_name
            type: string
            required: true
            description: Student last name
            -in: formData
            name: email
            type: string
            required: true
            description: Student email
            -in: formData
            name: _password_hash
            type: string
            required: true
            description: Student password
            -in: formData
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
                username = request.form['username'],
                first_name = request.form['first_name'],
                last_name = request.form['last_name'],
                email = request.form['email'],
                _password_hash = request.form['_password_hash'],
                profile_picture = request.form['profile_picture'],
            )
            db.session.add(new_student)
            db.session.commit()
            response_dict = new_student.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except Exception as e:
            print(f"Error creating student: {e}")
            return make_response(jsonify({"error": "Unable to create student", "details": str(e)}), 500)
    
class StudentByID(Resource):
    def get(self, id):
        """
        Get student by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the student to retrieve
        responses:
            200:
                description: Student data
            404:
                description: Student not found
        """
        response_dict = Student.query.filter_by(id=id).first()
        response = make_response(response_dict, 200)
        return response
    
    def patch(self, id):
        """
        Update student by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the student to update
            -in: body
            name: body
            schema:
                $ref: '#/definitions/Student'
        responses:
            200:
                description: Student successfully updated
            400:
                description: Invalid data or student not found
        """
        record = Student.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Student not found"}), 400)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data"}), 400)
        for attr, value in data.items():
            if hasattr(record, attr):
                setattr(record, attr, value)
        try:
            db.session.add(record)
            db.session.commit()
            response_dict = record.to_dict()
            return make_response(jsonify(response_dict), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to update student", "details": str(e)}), 500)
        
    def delete(self, id):
        """
        Delete student by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the student to delete
        responses:
            200:
                description: Student successfully deleted
            404:
                description: Student not found
        """
        record = Student.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Student not found"}), 400)
        try:
            db.session.delete(record)
            db.session.commit()
            response_dict = {"message": "Student successfully deleted"}
            return make_response(response_dict, 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete student", "details": str(e)}), 500)
