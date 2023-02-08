import os
from functools import reduce

from pymongo import MongoClient

mongodb_client = MongoClient(os.getenv('MONGO_URI', 'mongodb://mongo:27017/'))
students_db = mongodb_client.student_database
students = students_db.students


def add(student=None):
    # Check if student already exists
    if list(students.find({'$or': [
        {'student_id': student.student_id},
        {'first_name': student.first_name},
        {'last_name': student.last_name}
    ]})):
        return 'already exists', 409

    # Insert student into MongoDB collection
    students.insert_one(student.to_dict())
    return student.student_id


def get_by_id(student_id=None, subject=None):
    # Find student in MongoDB collection
    student = students.find_one({'student_id': student_id})
    if not student:
        return 'not found', 404

    # Return student, without exposing the internal MongoDB `_id` field
    return {key: student[key] for key in student.keys() if key != '_id'}


def delete(student_id=None):
    # Find student in MongoDB collection
    student = students.find_one({'student_id': student_id})
    if not student:
        return 'not found', 404

    # Delete student from MongoDB collection
    students.delete_one({'student_id': student_id})
    # Return no content and HTTP 204
    return None, 204
