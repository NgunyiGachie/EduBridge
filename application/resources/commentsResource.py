from database import db
from application.models.comments import Comment
from flask import jsonify, request, make_response
from flask_restful import Resource
from datetime import datetime

class CommentResource(Resource):

    def get(self):
        """
        Get all comments
        ---
        responses:
            200:
                description: A list of comments
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/Comment'
            500:
                description: Internal Server Error
        """
        try:
            comments = Comment.query.all()
            return jsonify([comment.to_dict() for comment in comments])
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server error"}, 500
        
    def post(self):
        """
        Create a new comment
        ---
        parameters:
            -in: formData
            name: discussion_id
            type: integer
            required: true
            description: Discussion ID for the comment
            -in: formData
            name: student_id
            type: integer
            required: true
            description: Student ID for the comment
            -in: formData
            name: instructor_id
            type: integer
            required: true
            description: Instructor ID for the comment
            -in: formData
            name: content
            type: string
            required: true
            description: Comment content
            -in: formData
            name: posted_at
            type: string
            format: date-time
            required: true
            description: Posted date for the comment
            -in: formData
            name: edited_at
            type: string
            format: date-time
            required: true
            description: Edited date for the comment
        responses:
            201:
                description: Comment successfully created
            400:
                description: Missing required field
            500:
                description: Internal server error
        """
        try:
            posted_date_str = request.form.get('posted_date')
            edited_date_str = request.form.get('edited_date')
            posted_date = datetime.fromisoformat(posted_date_str) if posted_date_str else datetime.now()
            edited_date = datetime.fromisoformat(edited_date_str) if edited_date_str else datetime.now()

            new_comment = Comment(
                discussion_id = request.form['discussion_id'],
                student_id = request.form['student_id'],
                instructor_id = request.form['instructor_id'],
                content = request.form['content'],
                posted_at = posted_date,
                edited_date = edited_date,
            )
            db.session.add(new_comment)
            db.session.commit()
            response_dict = new_comment.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except Exception as e:
            print(f"Error creating comment: {e}")
            return make_response(jsonify({"error": "Unable to create comment", "details": str(e)}), 500)
        
class CommentByID(Resource):

    def get(self, id):
        """
        Get comment by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the comment to retrieve
        responses:
            200:
                description: Comment data
            404:
                description: Comment not found
        """
        response_dict = Comment.query.filter_by(id=id).first()
        response = make_response(response_dict, 200)
        return response
    
    def path(self, id):
        """
        Update comment by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the comment to update
            -in: body
            name: body
            schema:
                $ref: '#/definitions/Comment'
        responses:
            200:
                description: Comment successfully updated
            400:
                description: Invalid data or comment not found
        """
        record = Comment.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Comment not found"}), 400)
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
            db.session.add(record)
            db.session.commit()
            response_dict = record.to_dict()
            return make_response(jsonify(response_dict), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to update comment", "details": str(e)}), 500)
        
    def delete(self, id):
        """
        Delete assignment by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the comment to delete
        responses:
            200:
                description: Comment successfully delete
            404:
                description: Comment not found
        """
        record = Comment.query.filter_by(id=id).first()
        if not record: 
            return make_response(jsonify({"error": "Comment not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            response_dict = {"message": "comment successfully deleted"}
            response = make_response(
                response_dict,
                200
            )
            return response
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete comment", "details": str(e)}), 500)
