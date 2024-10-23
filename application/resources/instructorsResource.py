"""
instructors_resource.py

This module defines the RESTful resource for managing instructors in the application.
"""

from flask import jsonify, request, make_response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from database import db
from application.models.instructors import Instructor


class InstructorResource(Resource):
    """Resource for managing multiple instructors."""

    def get(self):
        """
        Get all instructors
        ---
        responses:
            200:
                description: A list of instructors
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/Instructor'
            500:
                description: Internal Server Error
        """
        try:
            instructors = Instructor.query.all()
            return jsonify([instructor.to_dict() for instructor in instructors])
        except SQLAlchemyError as e:
            print(f"An SQLAlchemy error occurred: {e}")
            return {"message": "Internal server Error"}, 500
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {"message": "Internal server Error"}, 500

    def post(self):
        """
        Create a new instructor
        ---
        parameters:
            - in: formData
              name: name
              type: string
              required: true
              description: Instructor name
            - in: formData
              name: email
              type: string
              required: true
              description: Instructor email
            - in: formData
              name: _password_hash
              type: string
              required: true
              description: Instructor password
            - in: formData
              name: profile_picture
              type: string
              required: true
              description: Instructor profile picture
            - in: formData
              name: department
              type: string
              required: true
              description: Instructor department
            - in: formData
              name: bio
              type: string
              required: true
              description: Instructor bio
        responses:
            201:
                description: Instructor successfully created
            400:
                description: Missing required field
            500:
                description: Internal server error
        """
        try:
            new_instructor = Instructor(
                name=request.form['name'],
                email=request.form['email'],
                _password_hash=request.form['_password_hash'],
                profile_picture=request.form['profile_picture'],
                department=request.form['department'],
                bio=request.form['bio'],
            )
            db.session.add(new_instructor)
            db.session.commit()
            response_dict = new_instructor.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error creating instructor: {e}")
            return make_response(jsonify({"error": "Unable to create instructor", "details": str(e)}), 500)
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error creating instructor: {e}")
            return make_response(jsonify({"error": "Unable to create instructor", "details": str(e)}), 500)


class InstructorByID(Resource):
    """Resource for managing a specific instructor by ID."""

    def get(self, instructor_id):
        """
        Get instructor by ID
        ---
        parameters:
            - in: path
              name: instructor_id
              type: integer
              required: true
              description: The ID of the instructor to retrieve
        responses:
            200:
                description: Instructor data
            404:
                description: Instructor not found
        """
        instructor = Instructor.query.filter_by(id=instructor_id).first()
        if instructor is None:
            return make_response(jsonify({"error": "Instructor not found"}), 404)
        return make_response(jsonify(instructor.to_dict()), 200)

    def patch(self, instructor_id):
        """
        Update instructor by ID
        ---
        parameters:
            - in: path
              name: instructor_id
              type: integer
              required: true
              description: The ID of the instructor to update
            - in: body
              name: body
              schema:
                  $ref: '#/definitions/Instructor'
        responses:
            200:
                description: Instructor successfully updated
            400:
                description: Invalid data or instructor not found
        """
        record = Instructor.query.filter_by(id=instructor_id).first()
        if not record:
            return make_response(jsonify({"error": "Instructor not found"}), 404)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)
        for attr, value in data.items():
            if hasattr(record, attr):
                setattr(record, attr, value)
        try:
            db.session.commit()
            response_dict = record.to_dict()
            return make_response(jsonify(response_dict), 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error updating instructor: {e}")
            return make_response(jsonify({"error": "Unable to update instructor", "details": str(e)}), 500)
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error updating instructor: {e}")
            return make_response(jsonify({"error": "Unable to update instructor", "details": str(e)}), 500)

    def delete(self, instructor_id):
        """
        Delete instructor by ID
        ---
        parameters:
            - in: path
              name: instructor_id
              type: integer
              required: true
              description: The ID of the instructor to delete
        responses:
            200:
                description: Instructor successfully deleted
            404:
                description: Instructor not found
        """
        record = Instructor.query.filter_by(id=instructor_id).first()
        if not record:
            return make_response(jsonify({"error": "Instructor not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            return make_response({"message": "Instructor successfully deleted"}, 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error deleting instructor: {e}")
            return make_response(jsonify({"error": "Unable to delete instructor", "details": str(e)}), 500)
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error deleting instructor: {e}")
            return make_response(jsonify({"error": "Unable to delete instructor", "details": str(e)}), 500)
