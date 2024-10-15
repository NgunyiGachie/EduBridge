from database import db
from application.models.submission import Submission
from flask import jsonify, request, make_response
from flask_restful import Resource
from datetime import datetime

class SubmissionResource(Resource):
    def get(self):
        """
        Get all submissions
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
            return jsonify([submission.to_dict() for submission in submissions])
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server Error"}, 500
        
    def post(self):
        """
        Create a new submission
        ---
        parameters:
            -in: formData
            name: assignment_id
            type: integer
            required: true
            description: Assignment ID for the submission
            -in: formData
            name: student_id
            type: integer
            required: true
            description: Student ID for the submission
            -in: formData
            name: submission_info
            type: string
            required: true
            description: Submission information
            -in: formData
            name: grade_id
            type: integer
            required: true
            description: Grade ID for the submission
            -in: formData
            name: date
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
            date_str = request.form.get('date')
            date = datetime.isoformat(date_str) if date_str else datetime.now()
            new_submission = Submission(
                assignment_id = request.form['assignment_id'],
                student_id = request.form['student_id'],
                submission_info = request.form['submission_info'],
                grade_id = request.form['grade_id'],
                date = date,
            )
            db.session.add(new_submission)
            db.session.commit()
            response_dict = new_submission.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except Exception as e:
            print(f"Error creating submission: {e}")
            return make_response(jsonify({"error": "Unable to create assignment", "details": str(e)}), 500)

class SubmissionByID(Resource):
    def get(self, id):
        """
        Get submission by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the submission to retrieve
        responses:
            200:
                description: Submission data
            404:
                description: Submission not found
        """
        response_dict = Submission.query.filter_by(id=id).first()
        response = make_response(response_dict, 200)
        return response
    
    def patch(self, id):
        """
        Update submission by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the submission to update
            -in: body
            name: body
            schema:
                $ref: '#/definitions/Submission'
        responses:
            200:
                description: Submission successfully updated
            400:
                description: Invalid data or submission not found
        """
        record = Submission.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Submission not found"}), 400)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)
        for attr, value in data.items():
            if attr in ['date'] and value:
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
            return make_response(jsonify({"error": "Unable to update submission", "details": str(e)}), 500)
        
    def delete(self, id):
        """
        Delete submission by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the submission to delete
        responses:
            200:
                description: Submission successfully deleted
            404:
                description: Submission not found
        """
        record = Submission.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Submission not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            response_dict = {"message": "Submission successfully deleted"}
            response = make_response(
                response_dict,
                200
            ) 
            return response
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete submission", "details": str(e)}), 500)
        
