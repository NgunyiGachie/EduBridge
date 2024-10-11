from database import db
from application.models.course import Course
from flask import jsonify, request, make_response
from flask_restful import Resource

class CourseResource(Resource):

    def get(self):
        """
        Get all courses
        ---
        responses:
            200:
                description: A list of courses
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/Course'
            500:
                description: Internal Server Error
        """
        try:
            courses = Course.query.all()
            return jsonify([course.to_dict() for course in courses])
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": "Internal Server Error"}, 500
        
    def post(self):
        """
        Create a new course
        ---
        parameters:
        -in: formData
        name: course_info
        type: string
        required: true
        description: Course info
        -in: formData
        name: instructor_id
        type: integer
        required: true
        description: Instructor ID for course
        -in: formData
        name: schedule
        type: string
        format: JSON
        required: true
        description: Course schedule
    responses:
        201:
            description: Course successfully created
        400:
            description: Missing required field
        500:
            description: Internal server error
        """
        try:
            new_course = Course(
                course_info = request.form['course_info'],
                instructor_id = request.form['instructor_id'],
                schedule = request.form['schedule'],
            )
            db.session.add(new_course)
            db.session.commit()
            response_dict = new_course.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except KeyError as ke:
            print(f"Missing: {ke}")
            return make_response(jsonify({"error": f"Missing required field: {ke}"}), 400)
        except Exception as e:
            print(f"Error creating course: {e}")
            return make_response(jsonify({"error": "Unable to create course", "details": str(e)}), 500)
        
class CourseByID(Resource):

    def get(self, id):
        """
        Get course by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the course to retrieve
        responses:
            200:
                description: Course data
            404:
                description: Course not found
        """
        response_dict = Course.query.filter_by(id=id).first()
        response = make_response(response_dict, 200)
        return response
    
    def patch(self, id):
        """
        Update course by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the course to update
            -in: body
            name: body
            schema:
                $ref: '#/definitions/Course'
        responses:
            200:
                description: Course successfully updated
            400:
                description: Invalid data or course not found
        """
        record = Course.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "Course not found"}), 400)
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Invalid data format"}), 400)
        for attr, value in data.items():
            if hasattr(record, attr):
                setattr(record, attr, value)
        try:
            db.session.add(record)
            db.session.commit()
            response_dict = record.to_dict()
            return make_response(jsonify(response_dict), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to update course", "details": str(e)}), 500)

    def delete(self, id):
        """
        Delete course by ID
        ---
        parameters:
            -in: path
            name: id
            type: integer
            required: true
            description: The ID of the course to delete
        responses:
            200:
                description: Course successfully deleted
            404:
                description: Course not found
        """
        record = Course.query.filter_by(id=id).first()
        if not record:
            return make_response(jsonify({"error": "course not found"}), 404)
        try:
            db.session.delete(record)
            db.session.commit()
            response_dict = {"message": "course successfully deleted"}
            response = make_response(
                response_dict,
                200
            ) 
            return response
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": "Unable to delete course", "details": str(e)}), 500)
