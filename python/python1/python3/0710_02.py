class Counter:
    def __init__(self, initValue =0) :
        self.count = initValue  # 변수선언
    
        # 멤버 베소드 만들기
    def increment(self):
        self.count += 1

#사용

a = Counter(150)
a.increment
print(a.count)
b = Counter()
print(b.count)
