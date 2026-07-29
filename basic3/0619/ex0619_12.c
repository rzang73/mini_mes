#include <stdio.h>

int main() {
    char str[100];
    int length = 0;

    scanf("%s", str);

    while (str[length] != '\0') {
        length++;
    }

    printf("문자열 길이 : %d\n", length);
    printf("\n");
    
    return 0;
}