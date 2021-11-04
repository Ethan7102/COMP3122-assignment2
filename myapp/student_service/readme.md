# Overview of the Python flask app
This is a containerized python flask REST API using MongoDB as the backend database server. The python flask app communicates the MongoDB through a docker network ass1. It uses the various environment variables entered by the command 'docker run'  for passing the information about the MongoDB server’s hostname, port number, username and password. The app requires an available MongoDB server and the correct MongoDB server's information, otherwise, the app will fail, then print an error message and exit.  

The function of this app is to access students' data from the collection 'University ' in MongoDB, then present them in JSON format. It contains five endpoints as follows:

* /me: Return a JSON object with my own Student ID and Name.
```
curl localhost:9990/me
```

* /students: Return a JSON object with all the students’ attributes.
```
curl localhost:9990/students
```

* /students/<student_id>: Return a JSON object with the specified student. The student_id can be changed to other number.
```
curl localhost:9990/students/33333
```

* /takes: Return the attributes of all the students with the courses.
```
curl localhost:9990/takes
```

* /takes/<student_id>: Return a JSON object for the specified student. The student_id can be changed to other number.
```
curl localhost:9990/takes/33333
```

For all of the endpoints above, the API will return an error message using JSON format with an HTTP response code of 404 if no matching student record is found.

# Pull the image from the docker hub repository
```
docker pull polyu20035673d/student_svc
```

# Run the docker image
The arguments in the following command (MONGO_USERNAME, MONGO_PASSWORD, MONGO_SERVER_HOST and MONGO_SERVER_PORT) should be changed to the MongoDB server's setting if the current arguments do not meet the server's setting.
```
docker run --rm --network ass1 -e MONGO_USERNAME=comp3122 -e MONGO_PASSWORD=12345 -e MONGO_SERVER_HOST='mongo' -e MONGO_SERVER_PORT='27017' -p 9990:15000 polyu20035673d/student_svc
```
After running this command, the endpoints will be available including '/me', '/students', '/students/<student_id>, '/takes' and /'takes/<student_id>.

# Build a docker image by Dockerfile(another way to get the docker image)
```
docker build -t polyu20035673d/student_svc .
```