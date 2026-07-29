price = int(input('가격을 입력하세요: '))
card = input('카드의 종류를 입력하세요: ')
if price > 20000 and card == 'python':
    print(' 배송료가 없음')
else:
    print(' 배송료가 3000원')
