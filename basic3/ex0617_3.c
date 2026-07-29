#include <stdio.h>

int main() {
    int input = 0;       // 입력받을 생산량
    int total = 0;       // 누적 생산량

    while (1) {
        // 1. 생산량 입력받기
        printf("생산량 입력 : ");
        scanf("%d", &input);

        // 2. 누적 생산량 계산
        total += input;

        // 3. 누적 생산량이 1000개 이상인지 확인
        if (total >= 1000) {
            printf("\n생산 목표 달성!\n");
            break; // while 문 탈출
        }

        // 4. 목표 달성 전이라면 현재 누적 생산량 출력
        printf("현재 누적 생산량 : %d\n\n", total);
    }

    // 5. 최종 생산량 출력
    printf("최종 생산량 : %d\n", total);

    return 0;
}