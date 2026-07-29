
def main():
    print("20cm 피자 2개의 면적=", get_area(20)+get_area(20))
    print("30cm 피자 1개의 면적=", get_area(30))


def get_area(radius):
    if radius >0 :
        area = 3.14*radius**2
    else:    
        area = 0
    return area

main()

def get_sum(start, end):
	sum = 0
	for i in range(start, end+1):
		sum += i
	return sum



# 1과 10이 get_sum()의 인수가 된다. 
x = get_sum(1, 10)  

# 1과 20이 get_sum()의 인수가 된다. 
y = get_sum(1, 20);  
print(x)
print(y)

##########디폴트 인수#####################

def greet(name, msg="별일없죠?"):
	print("안녕 ", name + ', ' + msg)

greet("영희", "반가워")

#########################################

def varfunc(*args ): 
	print (args)

print("하나의 값으로 호출")
varfunc(10)

print("두개의 값으로 호출")
varfunc(10, 20)


print("여러 개의 값으로 호출")
varfunc(10, 20, 30)



#######가변인수################
def add(*numbers) :
	sum = 0
	for n in numbers:
		sum = sum + n
	return sum

print(add(10, 20))
print(add(10, 20, 30))
print(add(10, 20, 30, 40 ))
print(add(10, 20, 30, 40, 50 ))