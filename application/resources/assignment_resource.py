"""
Module for handling assignment endpoints.
"""

from datetime import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from database import db
from application.models.assignment import Assignment

class AssignmentResource(Resource):
    """
    Resource for handling Assignment-related CRUD operations.
    """

    def get(self):
        """
        Get all assignments
        ---
        responses:
            200:
                description: A list of assignments
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/Assignment'
            500:
                description: Internal Server Error
        """
        try:
            assignments = Assignment.query.all()
            return jsonify([assignment.to_dict() for assignment in assignments])
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server error"}, 500

    def post(self):
        """
        Create a new assignment
        ---
        parameters:
            - in: formData
              name: title
              type: string
              required: true
              description: Assignment title
            - in: formData
              name: description
              type: string
              required: true
              description: Assignment description
            - in: formData
              name: course_id
              type: integer
              required: true
              description: Course ID for the assignment
            - in: formData
              name: due_date
              type: string
              format: date-time
              required: true
              description: Due date for the assignment
            - in: formData
              name: total_points
              type: integer
              required: true
              description: Total points for the assignment
        responses:
            201:
                description: Assignment successfully created
            400:
                description: Missing required field
            500:
                description: Internal server error
        """
        try:
            due_date_str = request.form.get('due_date')
            due_date = datetime.fromisoformat(due_date_str) if due_date_str else datetime.now()

            new_assignment = Assignment(
                title=request.form['title'],
                description=request.form['description'],
                course_id=request.form['course_id'],
                due_date=due_date,
                total_points=request.form['total_points']
            )
            db.session.add(new_assignment)
            db.session.commit()
            response_dict = new_assignment.to_dict()
            return make_response(jsonify(response_dict), 201)

        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except SQLAlchemyError as e:
            print(f"Error creating assignment: {e}")
            return make_response(jsonify({"error": "Unable to create assignment", "details": str(e)}),
                                500)


class AssignmentByID(Resource):
    """
    Resource for handling assignment operations by ID.
    """

    def get(self, assignment_id):
        """
        Get assignment by ID
        ---
        parameters:
            - in: path
              name: assignment_id
              type: integer
              required: true
              description: The ID of the assignment to retrieve
        responses:
            200:
                description: Assignment data
            404:
                description: Assignment not found
        """
        assignment = Assignment.query.filter_by(id=assignment_id).first()
        if assignment:
            return make_response(assignment.to_dict(), 200)
        return make_response(jsonify({"error": "Assignment not found"}), 404)

    def patch(self, assignment_id):
        """
        Update assignment by ID
        ---
        parameters:
            - in: path
              name: assignment_id
              type: integer
              required: true
              description: The ID of the assignment to update
            - in: body
              name: body
              schema:
                $ref: '#/definitions/Assignment'
        responses:
            200:
                description: Assignment successfully updated
            400:
                description: Invalid data or assignment not found
        """
        record = Assignment.query.filter_by(id=assignment_id).first()
        if not record:
            return make_response(jsonify({"error": "Assignment not found"}), 404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)

        for attr, value in data.items():
            if attr == 'due_date' and value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    return make_response(jsonify({"error": "Invalid date format"}), 400)
            if hasattr(record, attr):
                setattr(record, attr, value)

        try:
            db.session.add(record)
            db.session.commit()
            return make_response(jsonify(record.to_dict()), 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to update assignment",
                                        "details": str(e)}), 500)

    def delete(self, assignment_id):
        """
        Delete assignment by ID
        ---
        parameters:
            - in: path
              name: assignment_id
              type: integer
              required: true
              description: The ID of the assignment to delete
        responses:
            200:
                description: Assignment successfully deleted
            404:
                description: Assignment not found
        """
        record = Assignment.query.filter_by(id=assignment_id).first()
        if not record:
            return make_response(jsonify({"error": "Assignment not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            return make_response({"message": "Assignment successfully deleted"},
                                200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete assignment",
                                        "details": str(e)}), 500)
