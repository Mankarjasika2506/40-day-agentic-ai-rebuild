from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()  # create an instance of FastAPI

class Student(BaseModel):  # define a Pydantic model for the Student data structure
    name: str
    marks: int

@app.get("/student")   # define a GET endpoint that returns a Student object
def get_student():
    return Student(name="Sara", marks=88)

@app.post("/student")  # define a POST endpoint that creates a new Student object
def create_student(student: Student):
    return{"received":student}