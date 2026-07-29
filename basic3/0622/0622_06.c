#include <stdio.h>
#include <string.h>

#define MAX_SIZE 50

int main() {
    char p_name[MAX_SIZE];
    char p_date[MAX_SIZE];
    char lot_number[MAX_SIZE * 2] = ""; // 안전하게 두 배 크기로 지정

    printf("제품입력명:\n");
    
    scanf("%s", p_name); // 공백 없는 단어(Motor 등) 입력에 최적화

    printf("생산일 : ");
    scanf("%s", p_date); // 생산일자(20260622 등) 입력
       
    strcpy(lot_number, p_name); 
    strcat(lot_number, "_");          
    strcat(lot_number, p_date); 

    printf("출력:\n");
    printf("LOT 번호 : %s\n", lot_number);

    return 0;
}