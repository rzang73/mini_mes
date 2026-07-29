#include <stdio.h>

int main()
{
    int age;
    char name[20];

    printf("나이입력:");
    scanf("%d", &age);

    printf("이름입력:");
    fgets(name);
    printf("나이: %d, 이름: %s/n)", age, name);
    

    return 0;
}