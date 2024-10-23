"""Discussion resource for handling discussion-related endpoints."""

from datetime import datetime  # Standard library imports should come first
from flask import jsonify, request, make_response
from flask_restful import Resource
from database import db
from application.models.discussion import Discussion


class DiscussionResource(Resource):
    """Resource for managing discussions."""

    def get(self):
        """
        Get all discussions.
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
        Create a new discussion.
        ---
        parameters:
            - in: formData
              name: title
              type: string
              required: true
              description: Discussion title
            - in: formData
              name: description
              required: true
              description: Discussion description
            - in: formData
              name: course_id
              type: integer
              required: true
              description: Course ID of the discussion
            - in: formData
              name: created_at
              type: string
              format: date-time
              required: true
              description: Creation date for the discussion
            - in: formData
              name: updated_at
              type: string
              format: date-time
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
            created_date = datetime.fromisoformat(created_date_str) if created_date_str else datetime.now()
            updated_at = datetime.fromisoformat(updated_at_str) if updated_at_str else datetime.now()

            new_discussion = Discussion(
                title=request.form['title'],
                description=request.form['description'],
                course_id=request.form['course_id'],
                created_at=created_date,
                updated_at=updated_at,
            )
            db.session.add(new_discussion)
            db.session.commit()
            response_dict = new_discussion.to_dict()
            return make_response(jsonify(response_dict), 201)
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required fields: {ke}"}), 400)
        except Exception as e:
            print(f"Error creating discussion: {e}")
            return make_response(jsonify({"error": "Unable to create discussion", "details": str(e)}), 500)


class DiscussionByID(Resource):
    """Resource for managing discussions by ID."""

    def get(self, discussion_id):
        """
        Get discussion by ID.
        ---
        parameters:
            - in: path
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
        discussion = Discussion.query.filter_by(id=discussion_id).first()
        if discussion:
            return make_response(jsonify(discussion.to_dict()), 200)
        return make_response(jsonify({"error": "Discussion not found"}), 404)

    def patch(self, discussion_id):
        """
        Update discussion by ID.
        ---
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The ID of the discussion to update
            - in: body
              name: body
              schema:
                  $ref: '#/definitions/Discussion'
        responses:
            200:
                description: Discussion successfully updated
            400:
                description: Invalid data or discussion not found
        """
        discussion = Discussion.query.filter_by(id=discussion_id).first()
        if not discussion:
            return make_response(jsonify({"error": "Discussion not found"}), 404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)

        for attr, value in data.items():
            if attr in ['created_at', 'updated_at'] and value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    return make_response(jsonify({"error": "Invalid date format"}), 400)
            if hasattr(discussion, attr):
                setattr(discussion, attr, value)

        try:
            db.session.commit()
            response_dict = discussion.to_dict()
            return make_response(jsonify(response_dict), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to update discussion", "details": str(e)}), 500)

    def delete(self, discussion_id):
        """
        Delete discussion by ID.
        ---
        parameters:
            - in: path
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
        discussion = Discussion.query.filter_by(id=discussion_id).first()
        if not discussion:
            return make_response(jsonify({"error": "Discussion not found"}), 404)

        try:
            db.session.delete(discussion)
            db.session.commit()
            return make_response({"message": "Discussion successfully deleted"}, 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete discussion", "details": str(e)}), 500)
