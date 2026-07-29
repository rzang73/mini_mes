class Car:
    def __init__(self, brand='차', speed =0):
        self.brand = brand
        self.speed = speed
    
    #메소드

    def brand_print(self):
        print('지금 차의 브랜드는=', self.brand)
    def speed_print(self):
        print('지금 차의 속도는=', self.speed)

#main 객체마을  
my_car = Car()  #생성자를 사용하면 객체가 탄생
hong_car = Car()
my_car.brand = 'BMW' # 생성 후 초기화
my_car.speed = '160' # 생성 후 초기화

my_car.brand_print()
hong_car.speed_print()


class Television:
	def __init__(self, channel, volume, on):
		self.channel = channel
		self.volume = volume
		self.on = on

	def show(self):
		print(self.channel, self.volume, self.on)

	def setChannel(self, channel):
		self.channel = channel

	def getChannel(self):
		return self.channel

t = Television(9, 10, True)
t.show()

t.setChannel(11)
t.show()

import math

# Circle 클래스를 정의한다. 
class Circle:
    def __init__(self, radius = 0):
        self.radius = radius

    def getArea(self):
        return  math.pi * self.radius * self.radius

    def getPerimeter(self):
        return 2 * math.pi * self.radius 

# Circle 객체를 생성한다. 
c = Circle(10)
print("원의 면적", c.getArea())
print("원의 면적", c.getPerimeter())


