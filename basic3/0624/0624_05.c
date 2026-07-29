#include <stdio.h>

int main() 
{
    char buffer[200]; // 키보드 입력을 임시로 저장할 공간

    // 1. 사용자로부터 문자열 입력받기
    printf("c.txt에 저장할 문자열을 입력하세요: ");
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) 
    {
        printf("입력 오류가 발생했습니다.\n");
        return 1;
    }

    // 2. 파일을 쓰기 모드("w")로 열기
    FILE *fp = fopen("c.txt", "w");

    // 3. 파일이 정상적으로 열렸는지 확인
    if (fp == NULL) 
    {
        printf("파일을 열 수 없습니다.\n");
        return 1; 
    }

    // 4. fgets로 입력받은 문자열을 파일에 기록
    fputs(buffer, fp);

    // 5. 파일 닫기
    fclose(fp);

    // 6. [추가] 입력한 문자열을 화면(모니터)에 다시 출력하여 확인하기
    printf("\n--- 입력 및 저장 완료 ---\n");
    printf("화면 출력 : %s", buffer);
    printf("c.txt 파일에 성공적으로 저장되었습니다.\n");

    return 0;
}