#include <stdio.h>
#include <stdlib.h>
#include <memory.h>

int main()
{
    int *pi; //변수는 pi
    
    pi = (int*)malloc(sizeof(int)); // Heap 메모리에 4bytes 정수 공간이 만들어짐
    *pi = 10;

    printf("%d\n", *pi);
    
    free(pi);  // 메모리 청소

    return 0;
}