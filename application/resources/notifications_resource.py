"""Module for handling notifications endpoints."""

from datetime import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from database import db
from application.models.notifications import Notification


class NotificationsResource(Resource):
    """Resource for handling notifications."""

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
            return jsonify([n.to_dict() for n in notifications])
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error fetching notifications: {e}")
            return {"message": "Internal server error"}, 500

    def post(self):
        """
        Create a new notification
        ---
        parameters:
            - in: formData
              name: title
              type: string
              required: true
              description: Notification title
            - in: formData
              name: message_body
              type: string
              required: true
              description: Notification message body
            - in: formData
              name: student_id
              type: integer
              required: true
              description: Student ID for the notification
            - in: formData
              name: instructor_id
              type: integer
              required: true
              description: Instructor ID for the notification
            - in: formData
              name: read_status
              type: string
              required: true
              description: Notification read status
            - in: formData
              name: sent_date
              type: string
              format: date-time
              required: true
              description: Notification sent date
            - in: formData
              name: read_date
              type: string
              format: date-time
              required: true
              description: Notification read date
        responses:
            201:
                description: Notification successfully created
            400:
                description: Missing required field
            500:
                description: Internal server error
        """
        try:
            sent_date_str = request.form.get('sent_date')
            read_date_str = request.form.get('read_date')
            sent_date = (
                datetime.fromisoformat(sent_date_str)
                if sent_date_str else datetime.now()
            )
            read_date = (
                datetime.fromisoformat(read_date_str)
                if read_date_str else datetime.now()
            )
            new_notification = Notification(
                title=request.form['title'],
                message_body=request.form['message_body'],
                student_id=request.form['student_id'],
                instructor_id=request.form['instructor_id'],
                read_status=request.form['read_status'],
                sent_date=sent_date,
                read_date=read_date,
            )
            db.session.add(new_notification)
            db.session.commit()
            response_dict = new_notification.to_dict()
            return make_response(jsonify(response_dict), 201)
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(
                jsonify({"error": f"Missing required field: {ke}"}), 400
            )
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating notification: {e}")
            return make_response(
                jsonify({"error": "Unable to create notification",
                        "details": str(e)}),
                500
            )
        except Exception as e:
            print(f"Unexpected error: {e}")
            return make_response(
                jsonify({"error": "Internal server error",
                        "details": str(e)}), 500
            )


class NotificationByID(Resource):
    """Resource for handling individual notifications by ID."""

    def get(self, notification_id):
        """
        Get notification by ID
        ---
        parameters:
            - in: path
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
        notification = Notification.query.filter_by(id=notification_id).first()
        if notification:
            return make_response(jsonify(notification.to_dict()), 200)
        return make_response(
            jsonify({"error": "Notification not found"}), 404
        )

    def patch(self, notification_id):
        """
        Update notification by ID
        ---
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The ID of the notification to update
            - in: body
              name: body
              schema:
                  $ref: '#/definitions/Notification'
        responses:
            200:
                description: Notification successfully updated
            400:
                description: Invalid data or notification not found
        """
        record = Notification.query.filter_by(id=notification_id).first()
        if not record:
            return make_response(jsonify({"error": "Notification not found"}),
                                404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}),
                                400)

        for attr, value in data.items():
            if attr in ['sent_date', 'read_date'] and value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    return make_response(jsonify({"error": "Invalid date format"}),
                                        400)
            if hasattr(record, attr):
                setattr(record, attr, value)

        try:
            db.session.commit()
            return make_response(jsonify(record.to_dict()), 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating notification: {e}")
            return make_response(
                jsonify({"error": "Unable to update notification",
                        "details": str(e)}), 500
            )
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error: {e}")
            return make_response(
                jsonify({"error": "Internal server error",
                        "details": str(e)}), 500
            )

    def delete(self, notification_id):
        """
        Delete notification by ID
        ---
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The ID of the notification to delete
        responses:
            200:
                description: Notification successfully deleted
            404:
                description: Notification not found
        """
        record = Notification.query.filter_by(id=notification_id).first()
        if not record:
            return make_response(jsonify({"error": "Notification not found"}),
                                404)

        try:
            db.session.delete(record)
            db.session.commit()
            return make_response({"message": "Notification deleted"}, 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting notification: {e}")
            return make_response(
                jsonify({"error": "Unable to delete notification",
                        "details": str(e)}), 500
            )
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error: {e}")
            return make_response(
                jsonify({"error": "Internal server error",
                        "details": str(e)}), 500
            )
