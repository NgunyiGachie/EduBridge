from database import db
from application.models.grades import Grade
from flask import jsonify, request, make_response
from flask_restful import Resource
from datetime import datetime

class GradesResource(Resource):
    def get(self):
        """
        Get all grades
        ---
        responses:
            200:
                description: A list of grades
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/Grade'
            500:
                description: Internal Server Error
        """
        try:
            grades = Grade.query.all()
            return jsonify([grade.to_dict() for grade in grades])
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server Error"}, 500
        
    def post(self):
        """
        create a new grade
        ---
        parameters:
            -in: formData
            name: student_id
            type: integer
            required: true
            description: Student ID for the grade
            -in: formData
            name: course_id
            type: integer
            required: true
            description: Course ID for the grade
            -in: formData
            name: grade
            type: integer
            required: true
            description: Grade
            -in: formData
            name: date_posted
            type: string
            format: date-time
            required: true
            description: Date posted for grade
        """
        try:
            date_posted_str = request.form.get('date_posted')
            date_posted = datetime.isoformat(date_posted_str) if date_posted_str else datetime.now()

            new_grade = Grade(
                student_id = request.form['student_id'],
                course_id = request.form['course_id'],
                grade = request.form['grade'],
                date_posted = date_posted,
            )
            db.session.add(new_grade)
            db.session.commit()
            response_dict = new_grade.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except Exception as e:
            print(f"Error creating grade: {e}")
            return make_response(jsonify({"error": "Unable to create grade", "details": str(e)}), 500)

class GradeByID(Resource):
    def get(self, id):
        """
        Get grade by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the grade to retrieve
        responses:
            200:
                description: Grade data
            404:
                description: Grade not found
        """
        response_dict = Grade.query.filter_by(id=id).first()
        response = make_response(response_dict, 200)
        return response
    
    def patch(self, id):
        """
        Update grade by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the grade to update
            -in: body
            name: body
            schema:
                $ref: '#/definitions/Grade'
        responses:
            200:
                description: Grade successfully updated
            400:
                description: Invalid data or grade not found
        """
        record = Grade.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Grade not found"}), 400)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)
        for attr, value in data.items():
            if attr in ['date_posted'] and value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    return make_response(jsonify({"error": "Invalid date format"}), 400)
            if hasattr(record, attr):
                setattr(record, attr, value)
        try:
            db.session.add(record)
            db.session.commit()
            response_dict = record.to_dict()
            return make_response(jsonify(response_dict), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to update grade", "details": str(e)}), 500)
        
    def delete(self, id):
        """
        Delete grade by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the grade to delete
        responses:
            200:
                description: Grade successfully deleted
            404:
                description: Grade not found
        """
        record = Grade.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Grade not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            response_dict = {"message": "assignment successfully deleted"}
            response = make_response(
                response_dict,
                200
            ) 
            return response
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete assignment", "details": str(e)}), 500)