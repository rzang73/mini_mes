class Student:
    def __init__(self, name= '학생', age= 18):
        self.__name =name
        self.__age = age

    def get_age(self):
        return self.__name
#main
hong = Student()
hong.__name = '홍길동'
print(hong.__name)
