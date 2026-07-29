#include <stdio.h>

int main()
{
    char ch;
    double db;
    int in;

    char *pc = &ch;
    double *pd = &db;

    printf("ch변수 자료형의 크기: %d\n", sizeof(ch));
    printf("db변수 자료형의 크기: %d\n", sizeof(db));
    printf("int변수 자료형의 크기: %d\n", sizeof(in));

    printf("ch 포인터 변수 자료형의 크기: %d\n", sizeof(&ch));
    printf("db 포인터 변수 자료형의 크기: %d\n", sizeof(&db));
    printf("int 포인터 변수 자료형의 크기: %d\n", sizeof(&in));


    return 0;
}