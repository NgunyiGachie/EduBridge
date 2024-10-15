from database import db
from application.models.discussion import Discussion
from flask import jsonify, request, make_response
from flask_restful import Resource
from datetime import datetime

class DiscussionResource(Resource):

    def get(self):
        """
        Get all discussions
        ---
        responses:
            200:
                description: A list of discussions
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/Discussion'
            500:
                description: Internal Server Error
        """
        try:
            discussions = Discussion.query.all()
            return jsonify([discussion.to_dict() for discussion in discussions])
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal Server Error"}, 500
        
    def post(self):
        """
        Create new discussion
        ---
        parameters:
            -in: formData
            name: title
            type: string
            required: true
            description: Discussion title
            -in: formData
            name: description
            required: true
            description: Discussion description
            -in: formData
            name: course_id
            type: integer
            required: true
            description: Course ID of the discussion
            -in: formData
            name: created_at
            type: string
            format: date-time
            required: true
            description: Creation date for the discussion
            -in: formData
            name: updated_at
            type: string
            formate: date-time
            required: true
            description: Update date for the discussion
        responses:
            201:
                description: Discussion successfully created
            400:
                description: Missing required field
            500:
                description: Internal Server Error
        """
        try:
            created_date_str = request.form.get('created_at')
            updated_at_str = request.form.get('updated_at')
            created_date = datetime.isoformat(created_date_str) if created_date_str else datetime.now()
            updated_at = datetime.isoformat(updated_at_str) if updated_at_str else datetime.now()

            new_discussion = Discussion(
                title = request.form['title'],
                description = request.form['description'],
                course_id = request.form['course_id'],
                created_at = created_date,
                updated_at = updated_at,
            )
            db.session.add(new_discussion)
            db.session.commit()
            response_dict = new_discussion.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required fields: {ke}"}), 400)
        except Exception as e:
            print(f"Error creating discussion: {e}")
            return make_response(jsonify({"error": f"Unable to create discussion", "details": str(e)}), 500)
        
class DiscussionByID(Resource):

    def get(self, id):
        """
        Get discussion by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the discussion to retrieve
        responses:
            200:
                description: Discussion data
            404:
                description: Discussion not found
        """
        response_dict = Discussion.query.filter_by(id=id).first()
        response = make_response(response_dict, 200)
        return response
    
    def patch(self, id):
        """
        Update discussion by ID
        ---
        parameters:
            -in: path
            name; id
            type: integer
            required: true
            description: The ID of the discussion to update
            -in: body
            name: body
            schema:
                $ref: '#/definitions/Discussion'
        responses:
            200:
                description: Discussion successfully updated
            400:
                description: Invalid data or discussion not found
        """
        record = Discussion.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Discussion not found"}), 400)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)
        for attr, value in data.items():
            if attr in ['created_at', 'updated_at'] and value:
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
            return make_response(jsonify({"error": "Unable to update discussion", "details": str(e)}), 500)
        
    def delete(self, id):
        """
        Delete discussion by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the discussion to delete
        responses:
            200:
                description: Discussion successfully deleted
            404:
                description: Discussion not found
        """
        record = Discussion.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Discussion not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            response_dict = {"message": "Discussion successfully deleted"}
            response = make_response(
                response_dict,
                200
            )
            return response
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete discussion", "details": str(e)}), 500)