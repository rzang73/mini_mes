try:
    with open("input.txt", "r") as infile:
        ch = infile.read(1)
    while ch != "" :
            print(ch)
            ch = infile.read(1)

except BaseException as e:
     print('에러가 발생했습니다.')