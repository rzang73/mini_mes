
#include <stdio.h>
#include <string.h>

typedef struct
{
    char id[5];    // 4자리 제품번호 + 널 문자('\0')
    char name[50];
    int qty;
} Product;

// 파일에서 중복된 번호나 이름이 있는지 검사하는 함수
int checkDuplicate(const char *searchId, const char *searchName)
{
    FILE *fp = fopen("products.txt", "r");
    if (fp == NULL) 
    {
        return 0; 
    }

    char line[100];
    char tempId[10];
    char tempName[50];
    int tempQty;
    int result = 0;

    while (fgets(line, sizeof(line), fp) != NULL) 
    {
        if (sscanf(line, "%[^,],%[^,],%d", tempId, tempName, &tempQty) == 3) 
        {
            if (strcmp(tempId, searchId) == 0) 
            {
                result = 1; // 번호 중복
                break;
            }
            if (strcmp(tempName, searchName) == 0) 
            {
                result = 2; // 제품명 중복
                break;
            }
        }
    }

    fclose(fp);
    return result;
}

int main() 
{
    Product p;
    char choice;

    while (1) 
    {
        // 1. 제품번호 입력 (4자리 형식 고정)
        printf("제품번호 입력 : ");
        fgets(p.id, sizeof(p.id), stdin);
        
        if (strchr(p.id, '\n') == NULL) 
        {
            while (getchar() != '\n');
        }
        p.id[strcspn(p.id, "\n")] = '\0'; // 개행 문자 제거

        // 2. 제품명 입력
        printf("제품명 입력 : ");
        fgets(p.name, sizeof(p.name), stdin);
        
        if (strchr(p.name, '\n') == NULL) 
        {
            while (getchar() != '\n');
        }
        p.name[strcspn(p.name, "\n")] = '\0'; 

        // 3. 중복 검사 실행
        int dupStatus = checkDuplicate(p.id, p.name);
        if (dupStatus == 1) 
        {
            printf("[오류] 중복된 번호입니다. 저장되지 않았습니다.\n\n");
            goto ask_continue;
        }
        else if (dupStatus == 2) 
        {
            printf("[오류] 중복된 제품입니다. 저장되지 않았습니다.\n\n");
            goto ask_continue;
        }

        // 4. 수량 입력
        printf("수량 입력 : ");
        scanf("%d", &p.qty);
        while (getchar() != '\n'); // scanf 직후 엔터 버퍼 청소

        // 5. 파일에 추가 기록 ("a" 모드)
        FILE *fp = fopen("products.txt", "a");
        if (fp != NULL) 
        {
            // [핵심 수정] 파일의 크기가 0보다 큰지(이미 데이터가 존재하는지) 검사
            fseek(fp, 0, SEEK_END);
            long fileSize = ftell(fp);
            
            // 만약 파일에 내용이 이미 있다면, 안전하게 새로운 줄(\n)을 먼저 확보합니다.
            if (fileSize > 0) 
            {
                // 기존 데이터의 맨 마지막 문자가 \n이 아닐 상황까지 대비하여 안전하게 처리
                fseek(fp, -1, SEEK_END);
                char lastChar = fgetc(fp);
                
                // 파일 포인터를 다시 끝으로 되돌림
                fseek(fp, 0, SEEK_END);
                if (lastChar != '\n') 
                {
                    fprintf(fp, "\n");
                }
            }

            // 새로운 라인에 깔끔하게 데이터 저장
            fprintf(fp, "%s,%s,%d\n", p.id, p.name, p.qty);
            fclose(fp);
            printf("-> [%s,%s,%d] 파일 추가 기록 완료!\n", p.id, p.name, p.qty);
        }
        else 
        {
            printf("파일 기록 중 오류가 발생했습니다.\n");
        }

    // 중복 및 입력 완료 후 분기점
    ask_continue:
        printf("계속 입력할까요? (Y/N) : ");
        scanf(" %c", &choice);
        while (getchar() != '\n'); // scanf 직후 엔터 버퍼 청소

        if (choice == 'n' || choice == 'N') 
        {
            printf("레코드 입력 완료\n");
            break;
        }
        printf("\n");
    }

    return 0;
}