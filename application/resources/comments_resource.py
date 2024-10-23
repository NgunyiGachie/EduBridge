"""
Module for handling comments endpoints.
"""

from datetime import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from database import db
from application.models.comments import Comment

class CommentResource(Resource):
    """Resource for comment-related operations."""

    def get(self):
        """Get all comments.

        ---
        responses:
          200:
            description: A list of comments
            schema:
              type: array
              items:
                $ref: '#/definitions/Comment'
          500:
            description: Internal server error
        """
        try:
            comments = Comment.query.all()
            return jsonify([comment.to_dict() for comment in comments])
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server error"}, 500

    def post(self):
        """Create a new comment.

        ---
        parameters:
          - name: discussion_id
            in: formData
            type: integer
            required: true
          - name: student_id
            in: formData
            type: integer
            required: true
          - name: instructor_id
            in: formData
            type: integer
            required: true
          - name: content
            in: formData
            type: string
            required: true
          - name: posted_date
            in: formData
            type: string
            format: date-time
            required: false
          - name: edited_date
            in: formData
            type: string
            format: date-time
            required: false
        responses:
          201:
            description: Comment successfully created
            schema:
              $ref: '#/definitions/Comment'
          400:
            description: Missing required field
          500:
            description: Unable to create comment
        """
        try:
            posted_date_str = request.form.get('posted_date')
            edited_date_str = request.form.get('edited_date')
            posted_date = datetime.fromisoformat(posted_date_str) if posted_date_str else datetime.now()
            edited_date = datetime.fromisoformat(edited_date_str) if edited_date_str else datetime.now()

            new_comment = Comment(
                discussion_id=request.form['discussion_id'],
                student_id=request.form['student_id'],
                instructor_id=request.form['instructor_id'],
                content=request.form['content'],
                posted_at=posted_date,
                edited_at=edited_date,
            )
            db.session.add(new_comment)
            db.session.commit()
            response_dict = new_comment.to_dict()
            return make_response(jsonify(response_dict), 201)
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to create comment",
                                        "details": str(e)}), 500)

class CommentByID(Resource):
    """Resource for comment operations by ID."""

    def get(self, comment_id):
        """Get comment by ID.

        ---
        parameters:
          - name: comment_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Comment found
            schema:
              $ref: '#/definitions/Comment'
          404:
            description: Comment not found
        """
        response_dict = Comment.query.filter_by(id=comment_id).first()
        if response_dict:
            return make_response(jsonify(response_dict.to_dict()), 200)
        return make_response(jsonify({"error": "Comment not found"}), 404)

    def patch(self, comment_id):
        """Update comment by ID.

        ---
        parameters:
          - name: comment_id
            in: path
            type: integer
            required: true
          - name: comment
            in: body
            schema:
              type: object
              properties:
                posted_at:
                  type: string
                  format: date-time
                edited_at:
                  type: string
                  format: date-time
                content:
                  type: string
        responses:
          200:
            description: Comment successfully updated
            schema:
              $ref: '#/definitions/Comment'
          400:
            description: Invalid data format
          404:
            description: Comment not found
          500:
            description: Unable to update comment
        """
        record = Comment.query.filter_by(id=comment_id).first()
        if not record:
            return make_response(jsonify({"error": "Comment not found"}), 404)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)
        for attr, value in data.items():
            if attr in ['posted_at', 'edited_at'] and value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    return make_response(jsonify({"error": "Invalid date format"}), 400)
                if hasattr(record, attr):
                    setattr(record, attr, value)
        try:
            db.session.commit()
            response_dict = record.to_dict()
            return make_response(jsonify(response_dict), 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to update comment",
                                          "details": str(e)}), 500)

    def delete(self, comment_id):
        """Delete comment by ID.

        ---
        parameters:
          - name: comment_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Comment successfully deleted
          404:
            description: Comment not found
          500:
            description: Unable to delete comment
        """
        record = Comment.query.filter_by(id=comment_id).first()
        if not record:
            return make_response(jsonify({"error": "Comment not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            return make_response({"message": "Comment successfully deleted"}, 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete comment",
                                          "details": str(e)}), 500)
