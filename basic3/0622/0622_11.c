#include <stdio.h>

int main() {
    
    int arr[5][5];
    int value = 1;

    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            arr[i][j] = value++;
        }
    }

    
    for (int i = 4; i >= 0; i--) {
        for (int j = 4; j >= 0; j--) {
            printf("%5d", arr[i][j]);
        }
        printf("\n"); 
    }

    return 0;
}