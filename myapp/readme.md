# launch services
In the base project base path, run the command "docker-compose up"

# To access the student-service
The function of the student-service is to access students' data from the collection 'University ' in MongoDB, then present them in JSON format. It contains the endpoints as follows:

* /me: Return a JSON object with my own Student ID and Name.
```
curl http://localhost:15000/me
```

* /students: Return a JSON object with all the students’ attributes.
```
curl http://localhost:15000/students
```

* /students/<student_id>: Return a JSON object with the specified student. The student_id can be changed to other number.
```
curl http://localhost:15000/students/33333
```

* /takes: Return the attributes of all the students with the courses.
```
curl http://localhost:15000/takes
```

* /takes/<student_id>: Return a JSON object for the specified student. The student_id can be changed to other number.
```
curl http://localhost:15000/takes/33333
```

* /add_student: Add a specified student
```
curl -X POST -v http://localhost:15000/add_student -H 'Content-Type: application/json' -d '{"student_id":"55555", "name":"Ian", "dept_name":"Comp. Sci.", "gpa":3.0}'
```

* /delete_student/<student_id>: Remove a specified student
```
curl -X DELETE -v http://localhost:15000/delete_student/55555
```

* /add_course: Add a course taken by a specified student 
```
curl -X POST -v http://localhost:15000/add_course -H 'Content-Type: application/json' -d '{"student_id":"33333", "course_id":"COMP2345", "credits":"3"}'
```

* /delete_course/<course_id>/<student_id>:Remove a specified course taken by a specified student
```
curl -X DELETE -v http://localhost:15000/delete_course/COMP1234/22222
```

# To access the metric exporter in your python flask app
Visit http://localhost:15000/metrics

# To access Prometheus
Visit http://localhost:9090

# To access Granfana
Visit http://localhost:3000
admin name: comp3122
password: 20035673D
In the search dashboards tab,  there is the preconfigured dashboard named MyDashboard.

# To run unit tests against your python flask app (running in the student_service container)
```
pytest tests/unit.py
```
The last test case will require root permission to stop the MongoDB container. Thus, you should enter your password when it is required or login to your root account first.