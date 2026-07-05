from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()  # create an instance of FastAPI

class Student(BaseModel):  # define a Pydantic model for the Student data structure
    name: str
    marks: int

students_db: dict[int, Student] = {} # in-memory database of students
next_id = 1     # global variable to keep track of the next student ID

@app.post("/students")  # define a POST endpoint that creates a new Student object
def create_student(student: Student):
    global next_id   # use the global variable next_id to assign a unique ID to each student
    students_db[next_id] = student
    created_id = next_id
    next_id += 1       # increment the next_id for the next student
    return {"id": created_id, "student": student}

@app.get("/students")  # define a GET endpoint that lists all students
def list_students():   # return a list of all students in the in-memory database
    return students_db

@app.get("/students/{id}")  # define a GET endpoint that retrieves a student by ID

def get_student(id: int):   # retrieve a student by ID from the in-memory database
    if id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[id]
  