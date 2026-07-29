#include <stdio.h>
#include <string.h> // strlen() 함수를 사용하기 위해 필요합니다.

int main() {
    char str[100];

    // 안내 문구 출력 후 fgets로 문자열 입력 받기
    printf("입력 : ");
    fgets(str, sizeof(str), stdin);

    // fgets로 인해 입력된 줄바꿈 문자('\n') 제거 과정
    int len = strlen(str);
    if (len > 0 && str[len - 1] == '\n') {
        str[len - 1] = '\0';
        len--; // 줄바꿈 문자를 제외했으므로 실제 문자열 길이도 1 줄여줍니다.
    }

    // 출력 문구 시작
    printf("출력 : ");

    // 마지막 문자(len - 1)부터 첫 번째 문자(0)까지 역순으로 반복 출력
    for (int i = len - 1; i >= 0; i--) {
        printf("%c", str[i]);
    }
    
    printf("\n"); // 최종 줄바꿈

    return 0;
}