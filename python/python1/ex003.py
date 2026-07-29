# 제어 변수를 선언한다. 

i = 1
sum = 0

# i 값이 10보다 작으면 반복
while i <= 10 :

	sum += i
	i = i + 1   #i++ 안됨!!

print("■ 합 계:", sum)
