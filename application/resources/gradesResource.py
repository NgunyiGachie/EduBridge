from datetime import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from database import db
from application.models.grades import Grade

class GradesResource(Resource):
    """
    Resource for handling grades.
    """

    def get(self):
        """
        Get all grades.
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
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server Error"}, 500

    def post(self):
        """
        Create a new grade.
        ---
        parameters:
            - in: formData
              name: student_id
              type: integer
              required: true
              description: Student ID for the grade
            - in: formData
              name: course_id
              type: integer
              required: true
              description: Course ID for the grade
            - in: formData
              name: grade
              type: integer
              required: true
              description: Grade
            - in: formData
              name: date_posted
              type: string
              format: date-time
              required: true
              description: Date posted for grade
        """
        try:
            date_posted_str = request.form.get('date_posted')
            date_posted = datetime.fromisoformat(date_posted_str) if date_posted_str else datetime.now()

            new_grade = Grade(
                student_id=request.form['student_id'],
                course_id=request.form['course_id'],
                grade=request.form['grade'],
                date_posted=date_posted,
            )
            db.session.add(new_grade)
            db.session.commit()
            response_dict = new_grade.to_dict()
            return make_response(jsonify(response_dict), 201)
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating grade: {e}")
            return make_response(jsonify({"error": "Unable to create grade", "details": str(e)}), 500)

class GradeByID(Resource):
    """
    Resource for handling operations on a single grade by ID.
    """

    def get(self, grade_id):
        """
        Get grade by ID.
        ---
        parameters:
            - in: path
              name: grade_id
              type: integer
              required: true
              description: The ID of the grade to retrieve
        responses:
            200:
                description: Grade data
            404:
                description: Grade not found
        """
        grade = Grade.query.filter_by(id=grade_id).first()
        if not grade:
            return make_response(jsonify({"error": "Grade not found"}), 404)
        return make_response(jsonify(grade.to_dict()), 200)

    def patch(self, grade_id):
        """
        Update grade by ID.
        ---
        parameters:
            - in: path
              name: grade_id
              type: integer
              required: true
              description: The ID of the grade to update
            - in: body
              name: body
              schema:
                  $ref: '#/definitions/Grade'
        responses:
            200:
                description: Grade successfully updated
            400:
                description: Invalid data or grade not found
        """
        record = Grade.query.filter_by(id=grade_id).first()
        if not record:
            return make_response(jsonify({"error": "Grade not found"}), 404)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)
        for attr, value in data.items():
            if attr == 'date_posted' and value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    return make_response(jsonify({"error": "Invalid date format"}), 400)
            if hasattr(record, attr):
                setattr(record, attr, value)
        try:
            db.session.commit()
            return make_response(jsonify(record.to_dict()), 200)
        except SQLAlchemyError as e:
            db.session.rollback()  # Roll back the session in case of error
            print(f"Error updating grade: {e}")
            return make_response(jsonify({"error": "Unable to update grade", "details": str(e)}), 500)

    def delete(self, grade_id):
        """
        Delete grade by ID.
        ---
        parameters:
            - in: path
              name: grade_id
              type: integer
              required: true
              description: The ID of the grade to delete
        responses:
            200:
                description: Grade successfully deleted
            404:
                description: Grade not found
        """
        record = Grade.query.filter_by(id=grade_id).first()
        if not record:
            return make_response(jsonify({"error": "Grade not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            return make_response({"message": "Grade successfully deleted"}, 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting grade: {e}")
            return make_response(jsonify({"error": "Unable to delete grade", "details": str(e)}), 500)
