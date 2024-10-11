from database import db
from application.models.attendance import Attendance
from flask import jsonify, request, make_response
from flask_restful import Resource
from datetime import datetime

class AttendanceResource(Resource):

    def get(self):
        """
        Get all attendances
        ---
        responses:
            200:
                description: A list of attendances
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/Attendance'
            500:
                description: Internal Server Error
        """
        try:
            attendances = Attendance.query.all()
            return jsonify([Attendance.to_dict() for attendance in attendances])
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server error"}, 500
        
    def post(self):
        """
        Create a new attendance
        ---
        parameters:
            -in: formData
            name: student_id
            type: integer
            required: true
            description: Student ID of the attendance
            -in: formData
            name: lecture_id
            type: integer
            required: true
            description: Lecture ID of the attendance
            -in: formData
            type: string
            required: true
            description: Attendance status of attendance
            -in: formData
            type: string
            format: date-time
            required: true
            description: Date of the attendance
        responses:
            201:
                description: Attendance successfully created
            400:
                description: Missing required field
            500:
                description: Internal server error
        """
        try:
            dates_str = request.form.get('dates')
            dates = datetime.fromisoformat(dates_str) if dates_str else datetime.now()
            new_attendance = Attendance(
                student_id = request.form['student_id'],
                lecture_id = request.form['lecture_id'],
                instructor_id = request.form['instructor_id'],
                attendance_status = request.form['attendance_status'],
                dates = dates
            )
            db.session.add(new_attendance)
            db.session.commit()
            response_dict = new_attendance.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required fields: {ke}"}, 400))
        except Exception as e:
            print(f"Error creating assignment: {e}")
            return make_response(jsonify({"error": "Unable to create assignment", "details": str(e)}))

class AttendanceByID(Resource):

    def get(self, id):
        """
        Get attendance by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the attendance to retrieve
        responses:
            200:
                description: Attendance data
            404:
                description: Attendance not found
        """
        response_dict = Attendance.query.filter_by(id=id).first()
        response = make_response(response_dict, 200)
        return response

    def path(self, id):
        """
        Update attendance by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the attendance to update
            -in: body
            name: body
            schema:
                $ref: '#/definitions/Attendance'
        responses:
            200:
                description: Attendance successfully updated
            400:
                description: Invalid data or attendance not found
        """
        record = Attendance.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Attendance not found"}), 400)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)
        for attr, value in data.items():
            if attr in ['dates'] and value:
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
            return make_response(jsonify({"error": "Unable to update attendance", "details": str(e)}), 500)

    def delete(self, id):
        """
        Delete attendance by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the attendance to delete
        responses:
            200:
                description: Attendance successfully deleted
            404:
                description: Attendance not found
        """
        record = Attendance.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Attendance not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            response_dict = {"message": "attendance successfully deleted"}
            response = make_response(
                response_dict,
                200
            )
            return response
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete attendance", "details": str(e)}), 500)