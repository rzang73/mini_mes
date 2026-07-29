#include <stdio.h>
#include <stdlib.h>

int main()
{
    int *arr;
    arr =(int*)malloc(sizeof(int)*10);
    //입력
    for(int i= 0; i<10; i++){
        arr[i] = i+1;

    }
    //출력
    for(int i= 0; i<10; i++){
        arr[i] = i+1;
        printf("%5d",arr[i]);    
    }

    return 0;
}
