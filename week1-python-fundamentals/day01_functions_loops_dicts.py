# 1. fuction with one parameter
def greet_student(name):
    return f"Hello, {name}! Ready for day 1?"
print(greet_student("Mack"))


# 2. function with multiplr parameters + default parameter
def calculate_grade(marks,total=100):
    percentage = marks/total*100
    return percentage 
print(calculate_grade(marks=85))
print(calculate_grade(marks=45, total=50))


# 3. for loop + dicts
students = [
    {"name": "Asha", "marks": 78},
    {"name": "Rohan", "marks": 45},
    {"name": "Priya", "marks": 92}
]
for student in students:
    print(f"student {student['name']}, marks {student['marks']}, Grade {calculate_grade(student['marks'])}")


# 4. Conditionals 
students = [
    {"name": "Asha", "marks": 78},
    {"name": "Rohan", "marks": 35},
    {"name": "Priya", "marks": 92}
]
for student in students:
    if student['marks'] >= 40:
        print(f"{student['name']} has passed with grade {calculate_grade(student['marks'])}")
    else:
        print(f"{student['name']} has failed with grade {calculate_grade(student['marks'])}")


# 5. try/except
students = [
    {"name": "Asha", "marks": 78},
    {"name": "Rohan", "marks": 35},
    {"name": "Priya", "marks": 92}
]
try:
    student = {"name": "Asha", "marks": 78}
    print(student["attendance"])
except KeyError:
    print(f"Attendance not found for {student['name']}")