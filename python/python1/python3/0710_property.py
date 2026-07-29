class Student:
    def __init__(self, name ='학생', age = 18):
        self.__name = age

    @property
    def name(self):
        print('안녕하세요')
        return self.__name
        
    @property
    def age(self):
        return self.__age   
    @name.setter
    def name(self, value):
        self.__name = value
    #암호화 압축 보안 동기화 로그
    @name.setter
    def age(self, value):
        self.__age = value

#main
hong = Student()
hong.name = '홍길동'
hong.age = 30
print(hong.name)  #property 사용
print(hong.age)



# class BankAccount:
#     def __init__(self):
#         self.__balance = 0

#     def withdraw(self, amount):
#         self.__balance -= amount
#         print("통장에 ", amount, "가 출금되었음")
#         return self.__balance

#     def deposit(self, amount):
#         self.__balance += amount
#         print("통장에서 ", amount, "가 입금되었음")
#         return self.__balance

# a = BankAccount()
# a.deposit(100)
# a.withdraw(10)
