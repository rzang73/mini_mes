#include <stdio.h>

int main() {
    int i = 5;     // 5의 배수이므로 5부터 시작
    int count = 0; // 5의 배수의 개수를 저장할 변수

    // 1부터 100까지 반복
    while (i <= 100) {
        printf("%d ", i); // 5의 배수 출력
        count++;          // 개수 1 증가
        i += 5;           // 다음 5의 배수로 이동 (5씩 증가)
    }

    // 줄바꿈 후 총 개수 출력
    printf("\n총 개수 = %d개\n", count);

    return 0;
}
