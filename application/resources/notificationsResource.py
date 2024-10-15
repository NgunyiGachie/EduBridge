from database import db
from application.models.notifications import Notification
from flask import jsonify, request, make_response
from flask_restful import Resource
from datetime import datetime

class NotificationsResource(Resource):
    def get(self):
        """
        Get all notifications
        ---
        responses:
            200:
                description: A list of notifications
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/Notification'
            500:
                description: Internal Server Error
        """
        try:
            notifications = Notification.query.all()
            return jsonify([notification.to_dict() for notification in notifications])
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal server Error"}, 500
        
    def post(self):
        """
        Create a new notification
        ---
        parameters:
            -in: formData
            name: title
            type: string
            required: true
            description: Notification title
            -in: formData
            name: message_body
            type: string
            required: true
            description: Notification message body
            -in: formData
            name: student_id
            type: integer
            required: true
            description: Student ID for the notification
            -in: formData
            name: instructor_id
            type: integer
            required: true
            description: Instructor ID for the notification
            -in: formData
            name: read_status
            type: string
            required: true
            description: Notification read status
            -in: formData
            name: sent_date
            type: string
            format: date-time
            required: true
            description: Notification sent date
            -in: formData
            name: read_date
            type: string
            format: date-time
            required: true
            description: Notification read date
        responses:
            201:
                description: Assignment successfully created
            400:
                description: Missing required field
            500:
                description: Internal server error 
        """
        try:
            sent_date_str = request.form.get('sent_date')
            read_date_str = request.form.get('read_date')
            sent_date = datetime.isoformat(sent_date_str) if sent_date_str else datetime.now()
            read_date = datetime.isoformat(read_date_str) if read_date_str else datetime.now()
            new_notification = Notification(
                title = request.form['title'],
                message_body = request.form['message_body'],
                student_id = request.form['student_id'],
                instructor_id = request.form['instructor_id'],
                read_status = request.form['read_status'],
                sent_date = sent_date,
                read_date = read_date,
            )
            db.session.add(new_notification)
            db.session.commit()
            response_dict = new_notification.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except Exception as e:
            print(f"Error creating notification: {e}")
            return make_response(jsonify({"error": "Unable to create notification", "details": str(e)}), 500)

class NotificationByID(Resource):
    def get(self, id):
        """
        Get notification by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the notification to retrieve
        responses:
            200:
                description: Notification data
            404:
                description: Notification not found
        """
        response_dict = Notification.query.filter_by(id=id).first()
        response = make_response(response_dict, 200)
        return response
    
    def patch(self, id):
        """
        Update notification by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the notification to update
            -in: body
            name: body
            schema:
                $ref: '#/definitions/Notification'
        responses:
            200:
                description: Notification successfully updated
            400:
                description: Invalid data or notification not found
        """
        record = Notification.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Assignment not found"}), 400)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)
        for attr, value in data.items():
            if attr in ['sent_date', 'read_date'] and value:
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
            return make_response(jsonify({"error": "Unable to update notification", "details": str(e)}), 500)
        
    def delete(self, id):
        """
        Delete notification by ID
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
        record = Notification.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Notification not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            response_dict = {"message": "Notification successfully deleted"}
            response = make_response(
                response_dict,
                200
            ) 
            return response
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete notification", "details": str(e)}), 500)

