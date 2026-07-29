
#include <stdio.h>

int main() {
    int cel;    // 정수형 변수
    double fah; // 실수형 변수

    scanf("%d", &cel);

   fah = (9 / 5.0 * cel) + 32.0;
    printf("%.1f\n", fah);
    return 0;
}
