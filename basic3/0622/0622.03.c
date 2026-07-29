#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BUFFER_SIZE 100

// 문자열 끝의 줄바꿈 기호(\n) 및 캐리지 리턴(\r)을 제거하는 안전한 함수
void trim_line(char *str) {
    size_t len = strlen(str);
    while (len > 0 && (str[len - 1] == '\n' || str[len - 1] == '\r')) {
        str[len - 1] = '\0';
        len--;
    }
}

int main() {
    char input_buffer[BUFFER_SIZE];
    
    printf("=== 스마트 팩토리 공정 로그 분석 시스템 ===\n");
    printf("로그 형식 예시 -> [LINE-A] CONVEYOR:RUNNING\n");
    printf("종료하려면 'EXIT'를 입력하세요.\n");
    printf("-------------------------------------------\n");

    while (1) {
        printf("\n로그 입력 >> ");
        fflush(stdout); // VS Code 출력 버퍼 비우기 (입력 프롬프트 꼬임 방지)
        
        // 1. 안전한 문자열 입력
        if (fgets(input_buffer, sizeof(input_buffer), stdin) == NULL) {
            break;
        }

        // 2. 공백 및 줄바꿈 정리
        trim_line(input_buffer);

        // 3. 종료 조건 검사 (대소문자 둘 다 지원)
        if (strcmp(input_buffer, "EXIT") == 0 || strcmp(input_buffer, "exit") == 0) {
            printf("시스템을 종료합니다.\n");
            break;
        }

        if (strlen(input_buffer) == 0) {
            continue;
        }

        // strtok 변형 방지를 위한 복사본 생성
        char log_copy[BUFFER_SIZE];
        strcpy(log_copy, input_buffer);

        // 4. 문자열 파싱 (공백과 콜론 기준)
        char *line_info = strtok(log_copy, " ");
        char *device_name = strtok(NULL, ":");
        char *status = strtok(NULL, ":");

        // 예외 처리: 데이터 포맷이 맞지 않을 때
        if (line_info == NULL || device_name == NULL || status == NULL) {
            printf("[오류] 올바르지 않은 로그 포맷입니다. 다시 입력하세요.\n");
            continue;
        }

        // 5. 검증 및 결과 출력
        if (strstr(line_info, "LINE") == NULL) {
            printf("[경고] 잘못된 라인 식별자입니다: %s\n", line_info);
            continue;
        }

        printf("\n[분석 결과 데이터]\n");
        printf(" -> 공정 라인: %s\n", line_info);
        printf(" -> 대상 장비: %s\n", device_name);
        printf(" -> 현재 상태: %s\n", status);

        if (strcmp(status, "ERROR") == 0 || strcmp(status, "STOP") == 0) {
            printf(" 🚨 [위험] %s 장비에 이상이 감지되었습니다! 현장 점검 바랍니다.\n", device_name);
        } else if (strcmp(status, "RUNNING") == 0) {
            printf(" ✅ [정상] %s 장비가 안정적으로 가동 중입니다.\n", device_name);
        } else {
            printf(" ⚠️ [알림] %s 장비가 알 수 없는 상태(%s) 코드입니다.\n", device_name, status);
        }
    }

    return 0;
}