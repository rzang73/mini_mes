#include <stdio.h>

int main()

{
 char grade;
 char name[20];
 

 printf("학점과 이름을 입력하세요:");
 
 scanf("%c", &grade);
 scanf("%s", name);

 printf("%s의 학점은 %c 입니다.\n", name, grade);
    
    return 0;
}