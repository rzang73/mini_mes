#include <stdio.h>

int main()
{
    char *pary[5];
    pary[0] = "dog";  // 문자열 상수는 포인터 변수
    pary[1] = "line";  // 문자열 상수는 포인터 변수
    pary[2] = "tiger";  // 문자열 상수는 포인터 변수
    pary[3] = "bear";  // 문자열 상수는 포인터 변수
    pary[4] = "pig";  // 문자열 상수는 포인터 변수

    for(int i=0; i<5; i++){
        printf("%s\n", pary[i]);
    }

    return 0;
}