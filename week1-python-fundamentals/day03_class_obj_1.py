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

asha = Student("Asha",78)
rohan = Student("Rohan",35)

print(asha.name,asha.marks,asha.is_passing())
print(rohan.name,rohan.marks,rohan.is_passing())

print(asha.is_passing())
print(rohan.is_passing())


print(asha.describe())
print(rohan.describe())