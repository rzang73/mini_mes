#include <stdio.h>
#include <stdlib.h> // rand(), srand() 함수를 사용하기 위한 라이브러리
#include <time.h>   // time() 함수를 사용하기 위한 라이브러리

int main() {
    // 실행할 때마다 진짜 랜덤한 값이 나오도록 실행 시간(time)을 시드 값으로 설정
    srand(time(NULL));

    // 3번 반복하는 for문
    for (int i = 1; i <= 30; i++) {
        /* rand() % 21은 0 ~ 20 사이의 숫자를 반환합니다.
           여기에 최소 온도인 30을 더하면 30 ~ 50 사이의 랜덤 온도가 됩니다.
        */
        int temperature = (rand() % 21) + 30;
        
        // 결과 출력
        printf("%d번: %d도\n", i, temperature);
    }

    return 0;
}