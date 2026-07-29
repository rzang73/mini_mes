class Counter:
    #생성자
    def __init__(self):  
        self.count = 0  #맴버 변수
    
    def increment(self):
        self.count += 1

#main

cnt = Counter()  #객체생성
cnt.increment()
print("카운터의 값=", cnt.count)

class Counter:
    def __init__(self) :
        self.count = 0
    def increment(self):
        self.count += 1
