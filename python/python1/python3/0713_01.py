class Car:    
    ## 멤버 생성자

    def __init__(self,speed, color, model, year, price):
        self.speed = speed
        self.color = color
        self.modle = model
        self.year = year
        self.price = price
    
    ## 멤버 메소드
    def drive(self):
        self.speed = 100
        print('자동차의 속도는', self.speed)

myCar = Car(0, "blue", "E-class", 2026, 50000000)


#print("자동차의 속도는", myCar.speed)
#print("자동차의 색상은", myCar.color)
#print("자동차의 모델은", myCar.model)
print("자동차의 연식:", myCar.year)
print("자동차의 가격:", myCar.price)
myCar.drive()
#print("자동차의 속도는", myCar.speed)


myTv = None
if myTv is None:
        print('현재 tv 가 없음.')
print(myTv)

# 텔레비전을 클래스로 정의한다. 
class Television:
	def __init__(self, channel, volume, on):
		self.channel = channel
		self.volume = volume
		self.on = on

	def show(self):
		print(self.channel, self.volume, self.on)

class App:
    def __init__(self):
        pass
    def setSilentMode(self, t):
        t.volume = 2    


# 전달받은 텔레비전의 음량을 줄인다. 

# setSilentMode()을 호출하여서 객체의 내용이 변경되는지를 확인한다. 
# Television() default 생성자
myTV = Television(11, 10, True);
myTV2 = Television(12, 13, False);
#setSilentMode(myTV)
myTV.show()
myTV2.show()