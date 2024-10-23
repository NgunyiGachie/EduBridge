from flask import jsonify, request, make_response
from flask_restful import Resource
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from database import db
from application.models.submission import Submission


class SubmissionResource(Resource):
    """Resource for handling submission-related requests."""

    def get(self):
        """
        Get all submissions.
        ---
        responses:
            200:
                description: A list of submissions
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/Submission'
            500:
                description: Internal Server Error
        """
        try:
            submissions = Submission.query.all()
            return jsonify(
                [submission.to_dict() for submission in submissions]
            )
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server Error"}, 500

    def post(self):
        """
        Create a new submission.
        ---
        parameters:
            - in: formData
              name: assignment_id
              type: integer
              required: true
              description: Assignment ID for the submission
            - in: formData
              name: student_id
              type: integer
              required: true
              description: Student ID for the submission
            - in: formData
              name: submission_info
              type: string
              required: true
              description: Submission information
            - in: formData
              name: grade_id
              type: integer
              required: true
              description: Grade ID for the submission
            - in: formData
              name: submission_date
              type: string
              format: date-time
              required: true
              description: Submission date
        responses:
             201:
                description: Submission successfully created
            400:
                description: Missing required field
            500:
                description: Internal server error
        """
        try:
            date_str = request.form.get('submission_date')
            submission_date = (
                datetime.fromisoformat(date_str)
                if date_str else datetime.now()
            )
            new_submission = Submission(
                assignment_id=request.form['assignment_id'],
                student_id=request.form['student_id'],
                submission_info=request.form['submission_info'],
                grade_id=request.form['grade_id'],
                date=submission_date,
            )
            db.session.add(new_submission)
            db.session.commit()
            response_dict = new_submission.to_dict()
            return make_response(jsonify(response_dict), 201)
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(
                jsonify({"error": f"Missing required field: {ke}"}), 400
            )
        except ValueError as ve:
            print(f"Error processing submission date: {ve}")
            return make_response(jsonify({"error": "Invalid date format"}), 400)
        except SQLAlchemyError as e:
            print(f"Error creating submission: {e}")
            return make_response(
                jsonify({"error": "Unable to create submission", "details": str(e)}),
                500
            )


class SubmissionByID(Resource):
    """Resource for handling submissions by ID."""

    def get(self, submission_id):
        """
        Get submission by ID.
        ---
        parameters:
            - in: path
              name: submission_id
              type: integer
              required: true
              description: The ID of the submission to retrieve
        responses:
            200:
                description: Submission data
            404:
                description: Submission not found
        """
        submission = Submission.query.filter_by(id=submission_id).first()
        if submission:
            return make_response(jsonify(submission.to_dict()), 200)
        return make_response(jsonify({"error": "Submission not found"}), 404)

    def patch(self, submission_id):
        """
        Update submission by ID.
        ---
        parameters:
            - in: path
              name: submission_id
              type: integer
              required: true
              description: The ID of the submission to update
            - in: body
              name: body
              schema:
                  $ref: '#/definitions/Submission'
        responses:
            200:
                description: Submission successfully updated
            400:
                description: Invalid data or submission not found
        """
        record = Submission.query.filter_by(id=submission_id).first()
        if not record:
            return make_response(jsonify({"error": "Submission not found"}), 404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)

        for attr, value in data.items():
            if attr == 'date' and value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    return make_response(
                        jsonify({"error": "Invalid date format"}),
                        400
                    )
            if hasattr(record, attr):
                setattr(record, attr, value)

        try:
            db.session.commit()
            return make_response(jsonify(record.to_dict()), 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(
                jsonify({"error": "Unable to update submission", "details": str(e)}),
                500
            )

    def delete(self, submission_id):
        """
        Delete submission by ID.
        ---
        parameters:
            - in: path
              name: submission_id
              type: integer
              required: true
              description: The ID of the submission to delete
        responses:
            200:
                description: Submission successfully deleted
            404:
                description: Submission not found
        """
        record = Submission.query.filter_by(id=submission_id).first()
        if not record:
            return make_response(jsonify({"error": "Submission not found"}), 404)

        try:
            db.session.delete(record)
            db.session.commit()
            return make_response(
                {"message": "Submission successfully deleted"}, 200
            )
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(
                jsonify({"error": "Unable to delete submission", "details": str(e)}),
                500
            )
