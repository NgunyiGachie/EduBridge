"""Resource for handling enrollments."""

from flask import jsonify, request, make_response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from database import db
from application.models.enrollments import Enrollment


class EnrollmentsResource(Resource):
    """Resource for managing enrollments."""

    def get(self):
        """
        Get all enrollments
        ---
        responses:
            200:
                description: A list of enrollments
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/Enrollment'
            500:
                description: Internal Server Error
        """
        try:
            enrollments = Enrollment.query.all()
            return jsonify([enrollment.to_dict() for enrollment in enrollments])
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal Server Error"}, 500

    def post(self):
        """
        Create a new enrollment
        ---
        parameters:
            - in: formData
              name: course_id
              type: integer
              required: true
              description: Course ID for the enrollment
            - in: formData
              name: student_id
              type: integer
              required: true
              description: Student ID for the enrollment
            - in: formData
              name: status
              required: true
              description: Enrollment status
        responses:
            201:
                description: Enrollment created successfully
            400:
                description: Missing required field
            500:
                description: Internal Server Error
        """
        try:
            new_enrollment = Enrollment(
                course_id=request.form['course_id'],
                student_id=request.form['student_id'],
                status=request.form['status'],
            )
            db.session.add(new_enrollment)
            db.session.commit()
            response_dict = new_enrollment.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required fields: {ke}"}), 400)
        except SQLAlchemyError as e:
            print(f"Error creating enrollment: {e}")
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to create enrollment", "details": str(e)}), 500)


class EnrollmentByID(Resource):
    """Resource for managing a specific enrollment by ID."""

    def get(self, enrollment_id):
        """
        Get enrollment by ID
        ---
        parameters:
            - in: path
              name: enrollment_id
              type: integer
              required: true
              description: The ID of the enrollment to retrieve
        responses:
            200:
                description: Enrollment data
            404:
                description: Enrollment not found
        """
        enrollment = Enrollment.query.filter_by(id=enrollment_id).first()
        if enrollment is None:
            return make_response(jsonify({"error": "Enrollment not found"}), 404)
        return make_response(jsonify(enrollment.to_dict()), 200)

    def patch(self, enrollment_id):
        """
        Update enrollment by ID
        ---
        parameters:
            - in: path
              name: enrollment_id
              type: integer
              required: true
              description: The ID of the enrollment to update
            - in: body
              name: body
              schema:
                  $ref: '#/definitions/Enrollment'
        responses:
            200:
                description: Enrollment successfully updated
            400:
                description: Invalid data or enrollment not found
        """
        record = Enrollment.query.filter_by(id=enrollment_id).first()
        if not record:
            return make_response(jsonify({"error": "Enrollment not found"}), 400)

        data = request.get_json()
        for attr, value in data.items():
            if hasattr(record, attr):
                setattr(record, attr, value)

        try:
            db.session.commit()
            response_dict = record.to_dict()
            return make_response(jsonify(response_dict), 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to update enrollment", "details": str(e)}), 500)

    def delete(self, enrollment_id):
        """
        Delete enrollment by ID
        ---
        parameters:
            - in: path
              name: enrollment_id
              type: integer
              required: true
              description: The ID of the enrollment to delete
        responses:
            200:
                description: Enrollment successfully deleted
            404:
                description: Enrollment not found
        """
        record = Enrollment.query.filter_by(id=enrollment_id).first()
        if not record:
            return make_response(jsonify({"error": "Enrollment not found"}), 404)

        try:
            db.session.delete(record)
            db.session.commit()
            return make_response({"message": "Enrollment successfully deleted"}, 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete enrollment", "details": str(e)}), 500)
