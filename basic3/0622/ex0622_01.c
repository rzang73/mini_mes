#include <stdio.h>

int main()
{
     char str1[80];// 문자열 사용을 위한 변수선언 1번째 방법
     char *str2;   // 포인터 변수로 문자열 사용. 2번째 방법

    printf("공백이 포함된 문자열 입력:");

    fgets(str1, sizeof(str1), stdin);
    
    printf("%s\n", str1);
   
    return 0;

}