# Mini Project 1: Student Grade Tracker (CLI)
class Student:
    def __init__(self, name, marks):
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


class Classroom:
    def __init__(self, section_name):
        self.section_name = section_name
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def average_marks(self):
        if not self.students:
            return 0
        total_marks = sum(student.marks for student in self.students)
        return total_marks / len(self.students)


class_9a = Classroom("9A")

while True:
    print("1. Add student")
    print("2. View all students")
    print("3. Save to file")
    print("4. Load from file")
    print("5. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter student name: ")
        marks = int(input("Enter student marks: "))
        s = Student(name, marks)
        class_9a.add_student(s)
        print(f"{name} added successfully!")

    elif choice == "2":
        for s in class_9a.students:
            print(s.describe())

    elif choice == "3":
        with open("students.txt", "w") as f:
            for s in class_9a.students:
                f.write(f"{s.name},{s.marks}\n")
        print("Saved to file!")

    elif choice == "4":
        class_9a.students = []
        with open("students.txt", "r") as f:
            lines = f.readlines()
        for line in lines:
            cleaned = line.strip()
            parts = cleaned.split(",")
            s = Student(parts[0], int(parts[1]))
            class_9a.add_student(s)
        print("Loaded from file!")
        
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice, try again")