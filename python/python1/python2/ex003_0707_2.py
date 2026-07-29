def display(msg = '반갑습니다', count = 5):
 for i in range(count):
    print(msg, end ='  ')

display()
display('어서오삼', 2)
display('안녕', 3)

def sub():
	return 1, 2, 3

a, b, c = sub()
print(a, b, c)
