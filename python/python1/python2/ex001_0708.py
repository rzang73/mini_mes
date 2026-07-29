questions =['name','quest','color']
answers =['Kim','파이썬','blue']
for q, a in zip(questions, answers):
	print(f"What is your {q}? It is {a}")


heroes = [ ] 				# 공백 리스트를 생성한다. 
heroes.append("아이언맨")		# 리스트에 ”아이언맨“을 추가한다. 
heroes.append("토르")			# 리스트에 ”토르“를 추가한다. 
heroes.insert(2, "원더우먼")			# 리스트에 ”토르“를 추가한다. 

print(heroes)
#heroes.pop(0)
heroes.remove("토르")

print(heroes)

salaries = [200, 250, 300, 280, 500]

def modify(values, factor) :
    for i in range(len(values)) :
        values[i] = values[i] * factor

print("인상전", salaries)
modify(salaries, 1.3)
print("인상후", salaries)


squares =[x*x for x in range(10) if x%2 ==0]
print(squares)
squares =[x*x for x in range(10) if x%2 ==1]
print(squares)

sq2 =[]
for x in range(10):
     sq2.append(x*x)
print(sq2)

prices = [135, -545, 922, 356, -992, 217]
mprices = [i if i > 0 else 0 for i in prices]
print(mprices)

words = ["All", "good", "things", "must", "come", "to", "an", "end."]
letters = [ w[0] for w in words ]
print(letters)

numbers = [x+y for x in ['a','b','c'] for y in ['x','y','z']]
print(numbers)

test = [x for x in range(100) if x % 2 == 0 and x % 3 == 0]
print(test)

list1=[10, 20, 30, 40, 50]

list2=[sum(list1[0:x+1]) for x in range(0, len(list1))]

print("원래 리스트: ",list1)
print("새로운 리스트: ",list2)

# 동적으로 2차원 리스트를 생성한다. 
rows = 3
cols = 5

s = [ ]
for row in range(rows): 
	s += [[0]*cols]		# 2차원 리스트끼리 합쳐진다. 

print("s =", s)


fruits =["apple","banana","grape"]
for index, value in enumerate(fruits):
	print(index +1, value)

nus = set()