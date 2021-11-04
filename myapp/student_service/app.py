from flask import Flask, jsonify, request
from flask.wrappers import Request
from pymongo import MongoClient
from bson.json_util import dumps
from bson.json_util import loads
import os
import pymongo
from urllib.parse import quote_plus
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app, path='/metrics')

def connect_db():
    # get mongodb's username, pwd, host name and port number from environment variables
    username = os.getenv('MONGO_USERNAME')
    password = os.getenv('MONGO_PASSWORD')
    host = os.getenv('MONGO_SERVER_HOST')
    port = os.getenv('MONGO_SERVER_PORT')

    # The flask API will print an error message and exit if the environment variables about MongoDB are not provided
    if username is None or password is None or host is None or port is None:
        print('The environment variables about MongoDB are not provided.')
        return 1

    # set url
    uri = "mongodb://%s:%s@%s:%s" % (quote_plus(username),
                                     quote_plus(password), quote_plus(host), quote_plus(port))

    # connect mongodb
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        client.server_info()  # connect to mongoDB to get the server info
    # MongoDB will be accessed unsuccessfully if the environment variables about MongoDB are incorrect.
    except pymongo.errors.ServerSelectionTimeoutError:
        print('Access failed. The environment variables about MongoDB are incorrect or the MongoDB server is not available.')
        return 1
    return client['university']

# Return a JSON object with my Student ID and Name.
@app.route('/me', methods=['GET'])
def get_me():
    # return my student information by JSON format
    return jsonify({"student_id": "20035673D", "name": "Wong Ming Yuen"}), 200

# Return a JSON object with all the students’ attributes
@app.route('/students', methods=['GET'])
def get_students():
    # connect DB
    db = connect_db()
    if db == 1:
        return jsonify({'error': 'The DB service is unavailable'}), 503
    students = db['student']
    # get all student data, disable _id coolumn and sort the students in ascending order of student_id
    cursor = students.find({}, {'_id': 0}).sort('student_id', 1)
    # iterate over to get a list of dicts
    dicts = [doc for doc in cursor]
    if len(dicts):  # if it is not empty
        return jsonify(dicts), 200
    else:  # print error message if no student records are found
        return jsonify({'error': 'not found'}), 404

# Return a JSON object with the specified student
@app.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    # connect DB
    db = connect_db()
    if db == 1:
        return jsonify({'error': 'The DB service is unavailable'}), 503
    students = db['student']
    # get student data by student ID, disable _id coolumn
    cursor = students.find({'student_id': {'$eq': student_id}}, {'_id': 0})
    # iterate over to get a list of dicts
    dicts = [doc for doc in cursor]
    if len(dicts):  # if it is not empty
        return jsonify(dicts), 200
    else:  # print error message if /no student with the specified student ID is found
        return jsonify({'error': 'not found'}), 404

# Return the attributes of all the students with the courses they are taking
@app.route('/takes', methods=['GET'])
def get_students_with_courses():
    # connect DB
    db = connect_db()
    if db == 1:
        return jsonify({'error': 'The DB service is unavailable'}), 503
    students = db['student']
    # aggregate two collection, the students were sorted in ascending order of student_id, the courses were sorted in ascending order of course_id
    cursor = students.aggregate([{'$lookup': {'from': 'takes', 'let': {'student_id': '$student_id'}, 'pipeline': [{'$match': {'$expr': {'$and': [{'$eq': ['$student_id', '$$student_id']}]}}}, {
                                '$project': {'_id': 0, 'student_id': 0}}, {'$sort': {'course_id': 1}}], 'as': 'student_takes'}}, {'$project': {'_id': 0}}, {'$sort': {'student_id': 1}}])
    # iterate over to get a list of dicts
    dicts = [doc for doc in cursor]
    if len(dicts):  # if it is not empty
        return jsonify(dicts), 200
    else:  # print error message if no student records are found
        return jsonify({'error': 'not found'}), 404

# Return a JSON object for the specified student
@app.route('/takes/<student_id>', methods=['GET'])
def get_student_with_courses(student_id):
    # connect DB
    db = connect_db()
    if db == 1:
        return jsonify({'error': 'The DB service is unavailable'}), 503
    students = db['student']
    # aggregate two collection, select the student by student_id,the students were sorted in ascending order of student_id, the courses were sorted in ascending order of course_id
    cursor = students.aggregate([{'$match': {'student_id': student_id}}, {'$lookup': {'from': 'takes', 'let': {'student_id': '$student_id'}, 'pipeline': [{'$match': {'$expr': {'$and': [{'$eq': [
                                '$student_id', '$$student_id']}]}}}, {'$project': {'_id': 0, 'student_id': 0}}, {'$sort': {'course_id': 1}}], 'as': 'student_takes'}}, {'$project': {'_id': 0}}, {'$sort': {'student_id': 1}}])
    # iterate over to get a list of dicts
    dicts = [doc for doc in cursor]
    if len(dicts):  # if it is not empty
        return jsonify(dicts), 200
    else:  # print error message if no student record with the specified student ID is found
        return jsonify({'error': 'not found'}), 404

# Add a specified student
@app.route('/add_student', methods=['POST'])
def add_studnet():
    # connect DB
    db = connect_db()
    if db == 1:
        return jsonify({'error': 'The DB service is unavailable'}), 503
    students = db['student']
    # get data
    data = request.data
    jdata = request.json

    # check whether both data exist in the JSON.
    if "student_id" in loads(data) and "name" in loads(data):
        student_id = jdata["student_id"]
    else:  # if either data is missed, the API will return an error message with code 400.
        return jsonify({'error': 'Missing data. The student id and student name must be included.'}), 400

    # search student data by student ID
    cursor = students.find({'student_id': {'$eq': student_id}})
    # iterate over to get a list of dicts
    dicts = [doc for doc in cursor]
    if len(dicts):  # return error message if this student exists in the database
        return jsonify({'error': 'This student already exists'}), 409
    else:  # insert the data into MongoDB if this student does not exist in the database
        students.insert_one(loads(data))
        return jsonify({'message': 'The insertion operation is successful.'}), 201
    

# Remove a specified student
@app.route('/delete_student/<student_id>', methods=['DELETE'])
def delete_user(student_id):
    # connect DB
    db = connect_db()
    if db == 1:
        return jsonify({'error': 'The DB service is unavailable'}), 503
    students = db['student']
    
    # search student data by student ID
    cursor = students.find({'student_id': {'$eq': student_id}})
    # iterate over to get a list of dicts
    dicts = [doc for doc in cursor]
    if len(dicts):  # delete the student record if this student exists in the database
        students.delete_one({"student_id": student_id})
        return jsonify({'message': 'The deletion operation is successful.'}), 200
    else:  # return error message if this student is not found in the database
        return jsonify({'error': 'This student is not found'}), 404

# Add a course taken by a specified student
@app.route('/add_course', methods=['POST'])
def add_course():
    # connect DB
    db = connect_db()
    if db == 1:
        return jsonify({'error': 'The DB service is unavailable'}), 503
    students = db['student']
    takes = db['takes']
    # get data
    data = request.data
    jdata = request.json

    # check whether both data exist in the JSON.
    if "student_id" in loads(data) and "course_id" in loads(data) and "credits" in loads(data):
        student_id = jdata["student_id"]
        course_id = jdata["course_id"]
    else:  # if either data is missed, the API will return an error message with code 400.
        return jsonify({'error': 'Missing data. The student id, course id and credits must be included.'}), 400

    # search student data by student ID
    cursor = students.find({'student_id': {'$eq': student_id}})
    # iterate over to get a list of dicts
    dicts = [doc for doc in cursor]

    if len(dicts) == 0:  # return error message if this student is not found in the database
        return jsonify({'error': 'This student is not found'}), 404
    else:
        cursor = takes.find(
            {'student_id': {'$eq': student_id}, 'course_id': {'$eq': course_id}})
        # iterate over to get a list of dicts
        dicts = [doc for doc in cursor]
        if len(dicts):  # return error message if this course with this student id exists in the database
            return jsonify({'error': 'This student already took this course.'}), 409
        else:  # insert the data into MongoDB
            takes.insert_one(loads(data))
            return jsonify({'message': 'The insertion operation is successful.'}), 201

# Remove a specified course taken by a specified student
@app.route('/delete_course/<course_id>/<student_id>', methods=['DELETE'])
def delete_course(student_id, course_id):
    # connect DB
    db = connect_db()
    if db == 1:
        return jsonify({'error': 'The DB service is unavailable'}), 503
    students = db['student']
    takes = db['takes']
    
    # search student data by student ID
    cursor = students.find({'student_id': {'$eq': student_id}})
    # iterate over to get a list of dicts
    dicts = [doc for doc in cursor]
    if len(dicts) == 0:  # return error message if this student is not found in the database
        return jsonify({'error': 'This student is not found'}), 404
    else:
        cursor = takes.find(
            {'student_id': {'$eq': student_id}, 'course_id': {'$eq': course_id}})
        # iterate over to get a list of dicts
        dicts = [doc for doc in cursor]
        if len(dicts) == 0:  # return error message if this course with this student id is not found in the database
            return jsonify({'error': 'This course record with this student id is not found.'}), 404
        else:  # delete the course record if this course with this student id exists in the database
            takes.delete_one(
                {"student_id": student_id, "course_id": course_id})
            return jsonify({'message': 'The deletion operation is successful.'}), 200


# start flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000, debug=False)
