from pydantic import BaseModel

class Address(BaseModel):
    city: str
    pincode: str

class Student(BaseModel):
    name: str
    address: list[Address] = None

s1 = Student(name="Klina", address=[Address(city="Virar", pincode="401303")])
print(type(s1))
print(s1)

# no pincode provided, should raise an error
s2 = None
try:
    s2 = Student(name="Slina", address=[Address(city="Virar")])
except Exception as e:
    print(e.errors())
if s2:
    print(s2)

# No pincode provided for another address in address list, should raise an error
s3 = None
try:
    s3 = Student(name="Alina", address=[{"city": "Virar", "pincode": "401303"}, {"city": "Mumbai"}])
except Exception as e:
    print(e.errors())
if s3:
    print(s3)
    


s4 = Student(name="Rohan")
print(s4.address)
print(type(s4.address))