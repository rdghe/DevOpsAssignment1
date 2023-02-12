import os

from pymongo import MongoClient

mongodb_client = MongoClient(os.getenv('MONGO_URI', 'mongodb://mongo:27017/'))
students_db = mongodb_client.student_database
students = students_db.students


def add(student=None):
    # Generate auto-incremental student_id
    # This is a naive implementation, and will not work in a distributed environment
    student_id = students.count_documents({}) + 1

    # Check if student already exists
    if students.count_documents({'$or': [
        {'first_name': student.first_name},
        {'last_name': student.last_name}
    ]}):
        return 'already exists', 409

    student_dict = student.to_dict()
    student_dict.update({'student_id': student_id})
    # Insert student into MongoDB collection
    students.insert_one(student_dict)
    return student_id, 200


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
    return student_id, 200
