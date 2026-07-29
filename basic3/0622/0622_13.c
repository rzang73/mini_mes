#include <stdio.h>

void print_num(int n);

int main() {
    int n;
    printf("자연수 입력:");
    scanf("%d", &n);
    
    for (int i = 1; i <= n; i++) {
        printf("%d ", i); 
    }
    printf("\n"); 

    return 0;
}

void print_num(int n){
    for(int i=1; i <=n; i++){
        printf("%d", i);
    }

}