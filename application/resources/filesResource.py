from database import db
from application.models.files import File
from flask import jsonify, request, make_response
from flask_restful import Resource
from datetime import datetime

class FilesResource(Resource):

    def get(self):
        """
        Get all files
        ---
        responses:
            200:
                description: A list of files
                schema:
                    type: array
                    items:
                    $ref: '#/definitions/File'
            500:
                description: Internal Server Error
        """
        try:
            files = File.query.all()
            return jsonify([file.to_dict() for file in files])
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal Server Error"}, 500
        
    def post(self):
        """
        Create a new file
        ---
        parameters:
            -in: formData
            name: file_info
            type: string
            required: true
            description: File information
            -in: formData
            name: related_to
            type: string
            required: true
            description: File related to
            -in: formData
            name: upload_date
            type: string
            format: date-time
            required: true
            description: File upload date
        responses:
            201:
                description: File successfully created
            400:
                description: Missing required field
            500:
                description: Internal server error 
        """
        try:
            upload_date_str = request.form.get('upload_date')
            upload_date = datetime.isoformat(upload_date_str) if upload_date_str else datetime.now()

            new_file = File(
                file_info = request.form['file_info'],
                related_to = request.form['related_to'],
                upload_date = upload_date,
            )
            db.session.add(new_file)
            db.sessin.commit()
            response_dict = new_file.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except Exception as e:
            print(f"Error creating file: {e}")
            return make_response(jsonify({"error": "Unable to create file", "details": str(e)}), 500)

class FileByID(Resource):

    def get(self, id):
        """
        Get file by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the file to retrieve
        responses:
            200:
                description: File data
            404:
                description: File not found
        """
        response_dict = File.query.filter_by(id=id).first()
        response = make_response(response_dict, 200)
        return response
    
    def patch(self, id):
        """
        Update file by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the file to update
            -in: body
            name: body
            schema:
                $ref: '#/definitions/File'
        responses:
            200:
                description: File successfully updated
            400:
                description: Invalid data or file not found
        """
        record = File.query.filter_by(id=id).first()
        if not record: 
            return make_response(jsonify({"Error": "File not found"}), 400)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data"}), 400)
        for attr, value in data.items():
            if attr in ['upload_date'] and value:
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
            return make_response(jsonify({"error": "Unable to update file", "details": str(e)}), 500)
        
    def delete(self, id):
        """
        Delete file by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the file to delete
        responses:
            200:
                description: File successfully deleted
            404:
                description: File not found
        """
        record = File.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "File not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            response_dict = {"message": "File successfully deleted"}
            response = make_response(
                response_dict,
                200
            ) 
            return response
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete file", "details": str(e)}), 500)

