def get_add(a, b, c):
     
    return  a + b + c

if __name__ == '__main__':
    
    print(get_add(3, 4, 5))



def treeful_add2(*num):
    
        return sum(num)

def main():
    
    result = treeful_add2(3, 4, 5, 6)
    
    print(f"3개 정수의 합: {result}")


if __name__ == "__main__":
    main()