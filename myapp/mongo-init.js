db.auth('comp3122', '12345')
db = db.getSiblingDB('university')

db.createCollection('student');

db.student.insertOne({'student_id':'33333', 'name':'Alice', 'dept_name':'Comp. Sci.', 'gpa':3.1});
db.student.insertOne({'student_id':'22222', 'name':'Bob', 'dept_name':'History.', 'gpa':2.0});
db.student.insertOne({'student_id':'11111', 'name':'Carol', 'dept_name':'History', 'gpa':2.1});


db.createCollection('takes');
db.takes.insertOne({'student_id':'33333', 'course_id':'COMP1234', 'credits':1});
db.takes.insertOne({'student_id':'22222', 'course_id':'COMP1234', 'credits':1});
db.takes.insertOne({'student_id':'22222', 'course_id':'COMP2345', 'credits':3});

db.takes.insertOne({'student_id':'22222', 'course_id':'COMP1345', 'credits':3});
db.takes.insertOne({'student_id':'22222', 'course_id':'COMP3345', 'credits':4});
db.takes.insertOne({'student_id':'22222', 'course_id':'COMP2345', 'credits':3});

db.student.insertOne({'student_id':'44444', 'name':'Nancy', 'phone':["1234","5678"], 'advisor':'Peter'});
db.takes.insertOne({'student_id':'44444', 'course_id':'EIE4567', 'name':'Introduction to ABCDE'});
db.takes.insertOne({'student_id':'44444', 'course_id':'COMP2345', 'grade':'A', 'semester':'202122A'});