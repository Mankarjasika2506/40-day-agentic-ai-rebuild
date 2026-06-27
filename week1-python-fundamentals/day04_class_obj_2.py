# path: week1-python-fundamentals/day04_class_obj_2.py
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
        return total_marks / len(self.students)

asha =Student("Asha",78)
rohan = Student("Rohan",35)

class_9a = Classroom("9A")
class_9a.add_student(asha)
class_9a.add_student(rohan)

print(class_9a.section_name)
for s in class_9a.students:
    print(s.describe())

print(f"Average marks for {class_9a.section_name}: {class_9a.average_marks()}")
    