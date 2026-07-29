#include <stdio.h>

int main()
{
    char name[50];

    printf("이름 입력 : ");

    fgets(name, sizeof(name), stdin);

    printf("%s", name);

    return 0;
}