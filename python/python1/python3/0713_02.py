class Student:
    st_number = 0
    def __init__(self, number =0):
        self.number =1
        Student.st_number += 1

st1 = Student(0)
st2 = Student(0)
st3 = Student(0)
print(st1.number)
print(st2.number)
print(st3.number)
print(Student.st_number)