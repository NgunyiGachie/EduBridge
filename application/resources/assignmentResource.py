from database import db
from application.models.assignment import Assignment
from flask import jsonify, request, make_response
from flask_restful import Resource
from datetime import datetime

class AssignmentResource(Resource):

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
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server Error"}, 500
    
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
            -in: formdata
            name: course_id
            type: integer
            required: true
            description: Course ID for the assignment
            -in: formData
            name: due_date
            type: string
            format: date-time
            required: false
            description: Due date for the assignment
            -in: formData
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
                title = request.form['title'],
                description = request.form['description'],
                course_id = request.form['course_id'],
                due_date = due_date,
                total_points = request.form['total_points']
            )
            db.session.add(new_assignment)
            db.session.commit()
            response_dict = new_assignment.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except Exception as e:
            print(f"Error creating assignment: {e}")
            return make_response(jsonify({"error": "Unable tp create assignment", "details": str(e)}), 500)

class AssignmentByID(Resource):

    def get(self, id):
        """
        Get assignment by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the assignment to retrieve
        responses:
            200:
                description: Assignment data
            404:
                description: Assignment not found
        """
        response_dict = Assignment.query.filter_by(id=id).first().to_dict()
        response = make_response(response_dict, 200)
        return response
    
    def patch(self, id):
        """
        Update assignment by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the assignment to update
            -in: body
            name: body
            schema:
                $ref: '#/definitions/Assignment'
        responses:
            200:
                description: Assignment successfully updated
            400:
                description: Invalid data or assignment not found
        """
        record = Assignment.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Assignment not found"}), 400)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)
        for attr, value in data.items():
            if attr in ['due_date'] and value:
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
            return make_response(jsonify({"error": "Unable to update assignment", "details": str(e)}), 500)
        
    def delete(self, id):
        """
        Delete assignment by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the assignment to delete
        responses:
            200:
                description: Assignment successfully deleted
            404:
                description: Assignment not found
        """
        record = Assignment.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Assignment not found"}), 404)
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