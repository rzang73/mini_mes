#include <stdio.h>

int main()
{
 int ary[5]= {10,20,30,40,50};
    int *pa = ary;
    int *pb = pa +3;

    printf("pa : %u\n", pa);
    printf("pb : %u\n", pb);

    pa++ ;
    printf("pa - pb : %d\n", pb - pa);

    printf("앞에 있는 배열 요소의 값: ");
    if (pa < pb) printf("%d\n", *pa);
    else printf("%d\n", *pb);
    
    //printf("%d\n");
    return 0;
}