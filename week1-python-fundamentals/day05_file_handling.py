# Write to file
with open("students.txt", "w") as f:
    f.write("Meera,88\n")
    f.write("John,65\n")

# Read from file
with open("students.txt", "r") as f:
    content = f.read()
print(content) 

# Append to file
with open("students.txt", "a") as f:
    f.write("Priya,92\n")

# Read all lines from file
with open("students.txt", "r") as f:
    lines = f.readlines()
print(lines)

# Remove whitespace and split lines into parts
line = "Meera,88\n"
cleaned = line.strip()
parts = cleaned.split(",")
print(parts)

# Create a dictionary for a student
student_dict = {"Name": parts[0], "Marks": int(parts[1])}
print(student_dict)

# Read all students from file and create a list of dictionaries
students_from_file = []

with open("students.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    cleaned = line.strip()
    parts = cleaned.split(",")
    student_dict = {"Name": parts[0], "Marks": int(parts[1])}
    students_from_file.append(student_dict)

print(students_from_file)

# Define a Student class
class Student:
    def __init__(self,name,marks):
        self.name = name
        self.marks = marks

    def is_passing(self):
        return self.marks >= 40
    
    def describe(self):
        if self.is_passing():
            status = "passing"
        else:
            status = "failing"
        return f"Student {self.name} scored {self.marks} and is {status}"

# New class to represent a classroom
class Classroom:
    def __init__(self,section_name):
        self.section_name = section_name
        self.students= []

    def add_student(self,student):
        self.students.append(student)

    def average_marks(self):
        if not self.students:
            return 0
        total_marks= sum(student.marks for student in self.students)
        return f"Average marks: {total_marks / len(self.students)}"

# Read students from file and create Student objects
students_from_file = []

with open("students.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    cleaned = line.strip()
    parts = cleaned.split(",")
    student_dict = {"Name": parts[0], "Marks": int(parts[1])}
    students_from_file.append(student_dict)

class_9a = Classroom("9A")
for student_dict in students_from_file:
    s = Student(student_dict['Name'], student_dict['Marks'])
    class_9a.add_student(s)

asha =Student("Asha",78)
rohan = Student("Rohan",35)
class_9a.add_student(asha)
class_9a.add_student(rohan)

# Print classroom details
print(f"Classroom: {class_9a.section_name}")

# Print average marks and student descriptions
print(class_9a.average_marks())
for s in class_9a.students:
    print(s.describe())


