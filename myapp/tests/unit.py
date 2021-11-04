import pytest
import requests
import subprocess


def test_get_students():
    response = requests.get("http://localhost:15000/students")
    assert response.status_code == 200


def test_get_first_student():
    # prepare the data for testing
    response = requests.get("http://localhost:15000/students")
    first_student_id = response.json()[0]["student_id"]

    response = requests.get(
        "http://localhost:15000/students/"+first_student_id)
    assert response.status_code == 200


def test_get_student_with_incorrect_id():
    incorrect_id = "xxxxx"
    response = requests.get("http://localhost:15000/students/"+incorrect_id)
    assert response.status_code == 404
    assert response.json() == {'error': 'not found'}


def test_get_takes():
    response = requests.get("http://localhost:15000/takes")
    assert response.status_code == 200


def test_get_takes_with_student_id():
    # prepare the data for testing
    response = requests.get("http://localhost:15000/takes")
    index = 0
    student_take = []
    while student_take == []:
        student_take = response.json()[index]["student_takes"]
        index += 1

    student_id = response.json()[index]["student_id"]
    response = requests.get("http://localhost:15000/takes/"+student_id)
    assert response.status_code == 200


def test_get_takes_with_incorrect_student_id():
    incorrect_student_id = "xxxxx"
    response = requests.get(
        "http://localhost:15000/takes/"+incorrect_student_id)
    assert response.status_code == 404
    assert response.json() == {'error': 'not found'}


def test_add_student():
    # prepare the situation for testing
    requests.delete("http://localhost:15000/delete_student/55555")

    data = {'student_id': '55555', 'name': 'Ian',
            'dept_name': 'Comp. Sci.', 'gpa': 3.0}
    response = requests.post("http://localhost:15000/add_student", json=data)
    assert response.status_code == 201
    assert response.json() == {
        'message': 'The insertion operation is successful.'}


def test_add_existing_student():
    # prepare the situation for testing
    requests.delete("http://localhost:15000/delete_student/55555")

    data = {'student_id': '55555', 'name': 'Ian',
            'dept_name': 'Comp. Sci.', 'gpa': 3.0}
    response = requests.post("http://localhost:15000/add_student", json=data)
    response = requests.post("http://localhost:15000/add_student", json=data)
    assert response.status_code == 409
    assert response.json() == {'error': 'This student already exists'}


def test_add_student_with_incomplete_data():
    # prepare the situation for testing
    requests.delete("http://localhost:15000/delete_student/55555")

    data = {'name': 'Ian', 'dept_name': 'Comp. Sci.', 'gpa': 3.0}
    response = requests.post("http://localhost:15000/add_student", json=data)
    assert response.status_code == 400
    assert response.json() == {
        'error': 'Missing data. The student id and student name must be included.'}


def test_delete_student():
    data = {'student_id': '55555', 'name': 'Ian',
            'dept_name': 'Comp. Sci.', 'gpa': 3.0}
    requests.post("http://localhost:15000/add_student", json=data)
    response = requests.delete("http://localhost:15000/delete_student/55555")
    assert response.status_code == 200
    assert response.json() == {
        'message': 'The deletion operation is successful.'}


def test_delete_student_with_nonexistent_student_id():
    nonexistent_student_id = "xxxxx"
    response = requests.delete(
        "http://localhost:15000/delete_student/"+nonexistent_student_id)
    assert response.status_code == 404
    assert response.json() == {'error': 'This student is not found'}


def test_add_course():
    # prepare the situation for testing
    requests.delete("http://localhost:15000/delete_course/COMP2345/33333")

    data = {'student_id': '33333', 'course_id': 'COMP2345',
            'credits': '3'}
    response = requests.post("http://localhost:15000/add_course", json=data)
    assert response.status_code == 201
    assert response.json() == {
        'message': 'The insertion operation is successful.'}


def test_add_course_with_incomplete_data():
    # prepare the situation for testing
    requests.delete("http://localhost:15000/delete_course/COMP2345/33333")

    data = {'course_id': 'COMP2345',
            'credits': '3'}
    response = requests.post("http://localhost:15000/add_course", json=data)
    assert response.status_code == 400
    assert response.json() == {
        'error': 'Missing data. The student id, course id and credits must be included.'}


def test_add_course_with_nonexistent_student_id():
    # prepare the situation for testing
    requests.delete("http://localhost:15000/delete_course/COMP2345/33333")

    nonexistent_student_id = "xxxxx"
    data = {'student_id': nonexistent_student_id, 'course_id': 'COMP2345',
            'credits': '3'}
    response = requests.post("http://localhost:15000/add_course", json=data)
    assert response.status_code == 404
    assert response.json() == {'error': 'This student is not found'}


def test_add_course_to_student_who_has_taken():
    # prepare the situation for testing
    requests.delete("http://localhost:15000/delete_course/COMP2345/33333")

    data = {'student_id': '33333', 'course_id': 'COMP2345',
            'credits': '3'}
    response = requests.post("http://localhost:15000/add_course", json=data)
    response = requests.post("http://localhost:15000/add_course", json=data)
    assert response.status_code == 409
    assert response.json() == {
        'error': 'This student already took this course.'}


def test_delete_course():
    # prepare the situation for testing
    data = {'student_id': '33333', 'course_id': 'COMP2345',
            'credits': '3'}
    requests.post("http://localhost:15000/add_course", json=data)

    response = requests.delete(
        "http://localhost:15000/delete_course/COMP2345/33333")
    assert response.status_code == 200
    assert response.json() == {
        'message': 'The deletion operation is successful.'}


def test_delete_course_with_nonexistent_student_id():
    nonexistent_student_id = "xxxxx"
    response = requests.delete(
        "http://localhost:15000/delete_course/COMP2345/"+nonexistent_student_id)
    assert response.status_code == 404
    assert response.json() == {'error': 'This student is not found'}


def test_delete_course_with_student_who_has_not_taken():
    # prepare the situation for testing
    requests.delete("http://localhost:15000/delete_course/COMP2345/33333")

    response = requests.delete(
        "http://localhost:15000/delete_course/COMP2345/33333")
    assert response.status_code == 404
    assert response.json() == {
        'error': 'This course record with this student id is not found.'}


def test_endpoint_without_dbserver():
    # prepare the situation for testing
    subprocess.check_call('sudo docker stop db', shell=True)
    requests.delete("http://localhost:15000/delete_student/55555")

    data = {'student_id': '55555', 'name': 'Ian',
            'dept_name': 'Comp. Sci.', 'gpa': 3.0}
    response = requests.post("http://localhost:15000/add_student", json=data)

    # reset the environment
    subprocess.check_call('sudo docker start db', shell=True)
    assert response.status_code == 503
    assert response.json() == {'error': 'The DB service is unavailable'}
