from database import db
from application.models.attendance import Attendance
from flask import jsonify, request, make_response
from flask_restful import Resource

class AttendanceResource(Resource):

    def get(self):
        try:
            attendances = Attendance.query.all()
            return jsonify([Attendance.to_dict() for attendance in attendances])
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server error"}, 500
