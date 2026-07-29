#include <stdio.h>

int main() {
    int choice; // 사용자가 입력한 메뉴 번호를 저장할 변수

    do {
        // 1. 메뉴판 화면 출력
        printf("\n========== [ 맛있는 요리 주문 ] ==========\n");
        printf("1. 김치찌개 (8,000원)\n");
        printf("2. 제육볶음 (9,000원)\n");
        printf("3. 돈까스   (9,500원)\n");
        printf("4. 짜장면   (7,000원)\n");
        printf("0. 주문 종료 (프로그램 종료)\n");
        printf("==========================================\n");
        printf("원하시는 요리의 번호를 입력하세요: ");
        
        // 2. 사용자 입력 받기
        scanf("%d", &choice);
        printf("\n"); // 줄바꿈으로 가독성 확보

        // 3. 사용자가 선택한 번호에 따른 처리 (switch문 활용)
        switch (choice) {
            case 1:
                printf("▶ [주문 완료] 얼큰한 '김치찌개'를 준비하겠습니다.\n");
                break;
            case 2:
                printf("▶ [주문 완료] 매콤한 '제육볶음'을 준비하겠습니다.\n");
                break;
            case 3:
                printf("▶ [주문 완료] 바삭한 '돈까스'를 준비하겠습니다.\n");
                break;
            case 4:
                printf("▶ [주문 완료] 달콤한 '짜장면'을 준비하겠습니다.\n");
                break;
            case 0:
                printf("▶ 이용해 주셔서 감사합니다. 주문을 종료합니다.\n");
                break;
            default:
                printf("❌ 잘못된 번호입니다. 0번부터 4번 사이의 숫자를 입력해 주세요.\n");
                break;
        }

    } while (choice != 0); // choice가 0이 아니면 무한 반복 (0이면 종료)

    return 0;
}
