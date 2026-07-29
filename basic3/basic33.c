#include <stdio.h>

int main() {
    // 세로줄(행)을 반복하는 바깥쪽 for문 (5번 반복)
    for (int i = 0; i < 5; i++) {
        
        // 가로줄(열)에 별을 출력하는 안쪽 for문 (5번 반복)
        for (int j = 0; j < 5; j++) {
            printf("*");
        }
        
        // 한 줄에 별 5개를 다 찍은 후 줄바꿈
        printf("\n");
    }

    return 0;
}