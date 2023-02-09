import os
import tempfile
import pymongo

from functools import reduce

# from tinydb import TinyDB, Query

mongoClient = pymongo.MongoClient("mongodb://mongo:27017/")
mydb = mongoClient["mydatabase"]
collection = mydb["students"]

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")


# student_db = TinyDB(db_file_path)


def add(student=None):
    queries = []
    # query = Query()
    # queries.append(query.first_name == student.first_name)
    # queries.append(query.last_name == student.last_name)
    # query = reduce(lambda a, b: a & b, queries)

    query = {"first_name": student.first_name, "last_name": student.last_name}
    res = collection.count_documents(query)
    # res = student_db.search(query)
    if res > 0:
        return 'already exists', 409

    # doc_id = student_db.insert(student.to_dict())
    doc_id = collection.insert_one(query).inserted_id
    student.student_id = str(doc_id)
    # return str(student.student_id)
    return student


def get_by_id(student_id=None, subject=None):
    # student = student_db.get(doc_id=int(student_id))
    student = collection.find_one({"student_id": student_id})
    if not student:
        return 'not found', 404
    # print(student)
    student['_id'] = str(student['_id'])
    return student


def delete(student_id=None):
    student = collection.find({"doc_id": int(student_id)})
    if not student:
        return 'not found', 404
    # student_db.remove(doc_ids=[int(student_id)])
    collection.delete_one({"doc_id": int(student_id)})
    return student_id