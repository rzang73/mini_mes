#include <stdio.h>

int main() {
    int num;
    int sum = 0;
  
    printf("자연수 입력:\n");
    scanf("%d", &num);
    
    for (int i = 1; i < num; i++) {
        if (num % i == 0) { 
            sum += i;       
        }
    }

    if (sum == num) {
        printf("yes\n");
    } 
    else {
        printf("no\n");
    }

    return 0;
}

