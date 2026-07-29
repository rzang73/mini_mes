#include <stdio.h>

int main() {
    // 크기가 10인 배열 선언 및 초기화 (마지막 index인 array[9]는 0으로 초기화됨)
    int array[10] = { 1, 2, 3, 4, 5, 6, 7, 8, 9 ,10};

    printf("홀수 값만 출력:\n");

        for (int i = 0; i < 10; i++) {
        
        if (array[i] % 2 != 0) { 
            printf("%d ", array[i]);
        }
    }
    printf("\n");
    return 0;
}