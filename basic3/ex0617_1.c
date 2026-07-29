#include <stdio.h>

int main() {
    printf("1 ~ 1000 숫자 중 30의 and 50의 배수 :\n");

    // 1부터 1000까지 반복
    for (int i = 1; i <= 1000; i++) {
        // i를 30으로 나눈 나머지 0, '그리고(&&)' 50으로 나눈 나머지 0
        if (i % 30 == 0 && i % 50 == 0) {
            printf("%d ", i);
        }
    }

    printf("\n");
    return 0;
}