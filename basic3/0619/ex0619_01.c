#include <stdio.h>

int main()
{
    int arr[5];
    //배열 초기화
    for(int i =0; i<5; i++){
        arr[i] = i+5;
        printf("%d ", arr[i]);

    }
    
    printf("\n");
    return 0;
}