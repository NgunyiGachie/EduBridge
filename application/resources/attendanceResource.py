from datetime import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from database import db
from application.models.attendance import Attendance


class AttendanceResource(Resource):
    """
    A resource to manage attendances.
    """

    def get(self):
        """
        Get all attendances.
        ---
        responses:
            200:
                description: A list of attendances.
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/Attendance'
            500:
                description: Internal Server Error.
        """
        try:
            attendances = Attendance.query.all()
            return jsonify([attendance.to_dict() for attendance in attendances])
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server error"}, 500

    def post(self):
        """
        Create a new attendance.
        ---
        parameters:
            -in: formData
            name: student_id
            type: integer
            required: true
            description: Student ID of the attendance.
            -in: formData
            name: lecture_id
            type: integer
            required: true
            description: Lecture ID of the attendance.
            -in: formData
            name: attendance_status
            type: string
            required: true
            description: Attendance status.
            -in: formData
            name: dates
            type: string
            format: date-time
            required: true
            description: Date of the attendance.
        responses:
            201:
                description: Attendance successfully created.
            400:
                description: Missing required field.
            500:
                description: Internal server error.
        """
        try:
            dates_str = request.form.get('dates')
            dates = datetime.fromisoformat(dates_str) if dates_str else datetime.now()
            new_attendance = Attendance(
                student_id=request.form['student_id'],
                lecture_id=request.form['lecture_id'],
                instructor_id=request.form['instructor_id'],
                attendance_status=request.form['attendance_status'],
                dates=dates
            )
            db.session.add(new_attendance)
            db.session.commit()
            response_dict = new_attendance.to_dict()
            return make_response(jsonify(response_dict), 201)
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required fields: {ke}"}), 400)
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating attendance: {e}")
            return make_response(jsonify({"error": "Unable to create attendance", "details": str(e)}), 500)


class AttendanceByID(Resource):
    """
    A resource to manage attendance by ID.
    """

    def get(self, attendance_id):
        """
        Get attendance by ID.
        ---
        parameters:
            -in: path
            name: attendance_id
            type: integer
            required: true
            description: The ID of the attendance to retrieve.
        responses:
            200:
                description: Attendance data.
            404:
                description: Attendance not found.
        """
        attendance = Attendance.query.filter_by(id=attendance_id).first()
        if attendance:
            return make_response(jsonify(attendance.to_dict()), 200)
        return make_response(jsonify({"error": "Attendance not found"}), 404)

    def patch(self, attendance_id):
        """
        Update attendance by ID.
        ---
        parameters:
            -in: path
            name: attendance_id
            type: integer
            required: true
            description: The ID of the attendance to update.
            -in: body
            name: body
            schema:
                $ref: '#/definitions/Attendance'
        responses:
            200:
                description: Attendance successfully updated.
            400:
                description: Invalid data or attendance not found.
        """
        attendance = Attendance.query.filter_by(id=attendance_id).first()
        if not attendance:
            return make_response(jsonify({"error": "Attendance not found"}), 400)

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)

        for attr, value in data.items():
            if attr == 'dates' and value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    return make_response(jsonify({"error": "Invalid date format"}), 400)
            if hasattr(attendance, attr):
                setattr(attendance, attr, value)

        try:
            db.session.add(attendance)
            db.session.commit()
            return make_response(jsonify(attendance.to_dict()), 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to update attendance", "details": str(e)}), 500)

    def delete(self, attendance_id):
        """
        Delete attendance by ID.
        ---
        parameters:
            -in: path
            name: attendance_id
            type: integer
            required: true
            description: The ID of the attendance to delete.
        responses:
            200:
                description: Attendance successfully deleted.
            404:
                description: Attendance not found.
        """
        attendance = Attendance.query.filter_by(id=attendance_id).first()
        if not attendance:
            return make_response(jsonify({"error": "Attendance not found"}), 404)

        try:
            db.session.delete(attendance)
            db.session.commit()
            return make_response(jsonify({"message": "Attendance successfully deleted"}), 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete attendance", "details": str(e)}), 500)
