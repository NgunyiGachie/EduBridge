from database import db
from application.models.lectures import Lecture
from flask import jsonify, request, make_response
from flask_restful import Resource
from datetime import datetime

class LecturesResource(Resource):
    def get(self):
        """
        Get all lectures
        ---
        responses:
            200:
                description: A list of lectures
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/Lecture'
            500:
                description: Internal Server Error
        """
        try:
            lectures = Lecture.query.all()
            return jsonify([lecture.to_dict() for lecture in lectures])
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server Error"}, 500
    
    def post(self):
        """
        create a new lecture
        ---
        parameters:
            -in: formData
            name: lecture_info
            type: string
            required: true
            description: Lecture info
            -in: formData
            name: instructor_id
            type: integer
            required: true
            description: Instructor ID of the lecture
            -in: formData
            name: schedule
            type: string
            format: JSON
            required: true
            description: Lecture schedule
            -in: formData
            name: created_at
            type: string
            format: date-time
            required: true
            description: Lecture creation date
            -in: formData
            name: updated_at
            type: string
            format: date-time
            required: true
            description; Lecture update date
        responses:
            201:
                description: Lecture successfully created
            400:
                description: Missing required field
            500:
                description: Internal server error 
        """
        try:
            created_at_str = request.form.get('created_at')
            updated_at_str = request.form.get('updated_at')
            created_at = datetime.isoformat(created_at_str) if created_at_str else datetime.now()
            updated_at = datetime.isoformat(updated_at_str) if updated_at_str else datetime.now()
            new_lecture = Lecture(
                lecture_info = request.form['lecture_info'],
                instructor_id = request.form['instructor_id'],
                schedule = request.form['schedule'],
                created_at = created_at,
                updated_at = updated_at,
            )
            db.session.add(new_lecture)
            db.session.commit()
            response_dict = new_lecture.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except Exception as e:
            print(f"Error creating assignment: {e}")
            return make_response(jsonify({"error": "Unable to create lecture", "details": str(e)}), 500)

class LectureByID(Resource):
    def get(self, id):
        """
        Get lecture by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the lecture to retrieve
        responses:
            200:
                description: Lecture data
            404:
                description: Lecture not found
        """
        response_dict = Lecture.query.filter_by(id=id).first()
        response = make_response(response_dict, 200)
        return response
    
    def patch(self, id):
        """
        Update lecture by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the lecture to update
            -in: body
            name: body
            schema:
                $ref: '#/definitions/Lecture'
        responses:
            200:
                description: Lecture successfully updated
            400:
                description: Invalid data or lecture not found
        """
        record = Lecture.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Lecture not found"}), 400)
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
            return make_response(jsonify({"error": "Unable to update lecture", "details": str(e)}), 500)
        
    def delete(self, id):
        """
        Delete lecture by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the lecture to delete
        responses:
            200:
                description: Lecture successfully deleted
            404:
                description: Lecture not found
        """
        record = Lecture.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Lecture not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            response_dict = {"message": "Lecture successfully deleted"}
            response = make_response(
                response_dict,
                200
            ) 
            return response
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete lecture", "details": str(e)}), 500)