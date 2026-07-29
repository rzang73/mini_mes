Temp = int(input('물의 온도을 입력하세요: '))

if 0 <Temp <= 100 :
    print('액체입니다')
elif Temp > 100 :
    print('기체입니다')
else:
    print('고체입니다.')