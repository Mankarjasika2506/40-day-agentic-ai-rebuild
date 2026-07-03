from pydantic import BaseModel, field_validator
from typing import Optional

class Student(BaseModel):
    name: str
    marks: int
    grade: Optional[str] = "N/A"

    @field_validator('marks')
    @classmethod
    def validate_marks(cls, value):
        if value < 0 or value > 100:
            raise ValueError("Marks must be between 0 and 100")
        return value
    
# Test cases for Student marks validation
# Test 1: valid
try:
    s1 = Student(name="Asha", marks=78)
    print(s1)
except Exception as e:
    print(f"Error: {e}")

# Test 2: too high
try:
    s2 = Student(name="Rihan", marks=150)
    print(s2)
except Exception as e:
    print(f"Error: {e}")

# Test 3: too low
try:
    s3 = Student(name="Priya", marks=-10)
    print(s3)
except Exception as e:
    print(f"Error: {e}")


# Valid student marks
s1 = Student(name="Esha", marks=78)
print(s1)
print(s1.name)
print(s1.marks)


# Invalid student marks - wrapped in try/except
try:
    s2 = Student(name="Rihan", marks="eighty")
    print(s2)
    print(s2.name)
    print(s2.marks)
except Exception as e:
    print(f"Error: {e}")


# Valid student with marks as string that can be converted to int
s3 = Student(name="Priya", marks="92")
print(s3)
print(s3.name)
print(s3.marks)
print(type(s3.marks))


# Test: no grade provided - should default to "N/A"
s4 = Student(name="Mack", marks=85)
print(s4.grade)


