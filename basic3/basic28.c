#include <stdio.h>

int main() {
    printf("1~100 사이의 3의 배수 또는 7의 배수:\n");
    
    for (int i = 1; i <= 100; i++) {
        // 3으로 나누어 떨어지거나 7로 나누어 떨어지는 경우
        if (i % 3 == 0 || i % 7 == 0) {
            printf("%d ", i);
        }
    }
    printf("\n");
    
    return 0;
}