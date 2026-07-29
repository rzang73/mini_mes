#include <stdio.h>

// 출력을 담당하는 함수 선언
void printf_result(int *pa)
{
    int i;
    for (i = 0; i < 3; i++)
    {
        printf("%5d", pa[i]);
    }
    printf("\n");
}

int main()
{
    int ary[3] = {10,20,30};
    int *pa = ary;

    *pa = 10;
    *(pa + 1) = 20;
    pa[2] = pa[0] + pa[1];
    
    // printf_result 함수를 호출하면서 포인터 pa를 전달
    printf_result(pa);

    return 0;
}