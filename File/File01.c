#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PRODUCTS 100

typedef struct
{
    char id[5];    
    char name[50];
    int qty;
    int price;     
    char lot[30];  
} Product;

Product* db[MAX_PRODUCTS];
int productCount = 0;

// 1. [수정] 파일 로드 시 헤더 유무를 정확히 판별하여 데이터 유실을 방지하는 함수
void loadFromFile()
{
    FILE *fp = fopen("products.txt", "r");
    if (fp == NULL) return; 

    char line[200];

    // 첫 번째 줄을 읽어옵니다.
    if (fgets(line, sizeof(line), fp) == NULL) {
        fclose(fp);
        return;
    }

    // [핵심 수정] 첫 번째 줄에 "id" 문자열이 포함되어 있는지 검사합니다.
    // "id"가 포함되어 있다면 헤더이므로 데이터를 읽지 않고 다음 줄로 넘어갑니다.
    // 만약 "id"가 없다면 헤더 없이 데이터(예: 0001,...)로 시작하는 것이므로 바로 파싱합니다.
    if (strstr(line, "id") == NULL)
    {
        char tempId[10], tempName[50], tempLot[30];
        int tempQty, tempPrice;

        if (sscanf(line, "%[^,],%[^,],%d,%d,%s", tempId, tempName, &tempQty, &tempPrice, tempLot) >= 5)
        {
            Product *p = (Product*)malloc(sizeof(Product));
            strcpy(p->id, tempId);
            strcpy(p->name, tempName);
            p->qty = tempQty;
            p->price = tempPrice;
            strcpy(p->lot, tempLot);
            db[productCount++] = p;
        }
    }

    // 두 번째 줄부터 끝까지 데이터를 읽어 포인터 배열에 담습니다.
    while (fgets(line, sizeof(line), fp) != NULL && productCount < MAX_PRODUCTS)
    {
        char tempId[10], tempName[50], tempLot[30];
        int tempQty, tempPrice;

        if (sscanf(line, "%[^,],%[^,],%d,%d,%s", tempId, tempName, &tempQty, &tempPrice, tempLot) >= 5)
        {
            Product *p = (Product*)malloc(sizeof(Product));
            strcpy(p->id, tempId);
            strcpy(p->name, tempName);
            p->qty = tempQty;
            p->price = tempPrice;
            strcpy(p->lot, tempLot);

            db[productCount++] = p;
        }
    }
    fclose(fp);
}

// 2. 메모리의 데이터를 파일에 저장하는 함수 (fseek로 맨 앞에 항상 헤더 강제 삽입)
void saveToFile()
{
    FILE *fp = fopen("products.txt", "w+");
    if (fp == NULL)
    {
        printf("파일을 저장할 수 없습니다.\n");
        return;
    }

    // fseek을 사용하여 파일의 가장 처음(SEEK_SET)으로 이동한 뒤 헤더 삽입
    fseek(fp, 0, SEEK_SET);
    fprintf(fp, "id,name,qty,price,lot\n");

    // 데이터 저장
    for (int i = 0; i < productCount; i++)
    {
        fprintf(fp, "%s,%s,%d,%d,%s\n", db[i]->id, db[i]->name, db[i]->qty, db[i]->price, db[i]->lot);
    }

    fclose(fp);
}

// 중복 검사 함수
int checkDuplicate(const char *searchId, const char *searchName)
{
    for (int i = 0; i < productCount; i++)
    {
        if (strcmp(db[i]->id, searchId) == 0) return 1; 
        if (strcmp(db[i]->name, searchName) == 0) return 2; 
    }
    return 0;
}

// 삽입(Create) 함수
void insertProduct()
{
    if (productCount >= MAX_PRODUCTS)
    {
        printf("[오류] 저장 공간이 가득 찼습니다.\n");
        return;
    }

    Product temp;
    char date[9], seq[4];

    printf("\n--- 제품 등록 ---\n");
    printf("제품번호 입력 : ");
    fgets(temp.id, sizeof(temp.id), stdin);
    if (strchr(temp.id, '\n') == NULL) while (getchar() != '\n');
    temp.id[strcspn(temp.id, "\n")] = '\0';

    printf("제품명 입력 : ");
    fgets(temp.name, sizeof(temp.name), stdin);
    if (strchr(temp.name, '\n') == NULL) while (getchar() != '\n');
    temp.name[strcspn(temp.name, "\n")] = '\0';

    int dup = checkDuplicate(temp.id, temp.name);
    if (dup == 1) { printf("[오류] 중복된 번호입니다.\n"); return; }
    if (dup == 2) { printf("[오류] 중복된 제품입니다.\n"); return; }

    printf("수량 입력 : ");
    scanf("%d", &temp.qty); while (getchar() != '\n');
    printf("단가 입력 : ");
    scanf("%d", &temp.price); while (getchar() != '\n');

    printf("생산일자 입력 (8자리, 예: 20260624) : ");
    fgets(date, sizeof(date), stdin);
    if (strchr(date, '\n') == NULL) while (getchar() != '\n');
    date[strcspn(date, "\n")] = '\0';

    printf("추가 번호 입력 (3자리, 예: 001) : ");
    fgets(seq, sizeof(seq), stdin);
    if (strchr(seq, '\n') == NULL) while (getchar() != '\n');
    seq[strcspn(seq, "\n")] = '\0';

    sprintf(temp.lot, "LOT%s%s", date, seq);

    Product *newP = (Product*)malloc(sizeof(Product));
    *newP = temp;
    db[productCount++] = newP;

    printf("-> 메모리에 추가 완료! (종료 시 파일에 일괄 반영됩니다.)\n");
}

// 수정(Update) 함수
void updateProduct()
{
    char searchId[5];
    printf("\n--- 제품 정보 수정 ---\n");
    printf("수정할 제품번호(4자리) 입력 : ");
    fgets(searchId, sizeof(searchId), stdin);
    if (strchr(searchId, '\n') == NULL) while (getchar() != '\n');
    searchId[strcspn(searchId, "\n")] = '\0';

    for (int i = 0; i < productCount; i++)
    {
        if (strcmp(db[i]->id, searchId) == 0)
        {
            printf("현재 정보: [%s] 제품명:%s, 수량:%d, 단가:%d, LOT:%s\n", db[i]->id, db[i]->name, db[i]->qty, db[i]->price, db[i]->lot);
            printf("새로운 수량 입력 : ");
            scanf("%d", &db[i]->qty); while (getchar() != '\n');
            printf("새로운 단가 입력 : ");
            scanf("%d", &db[i]->price); while (getchar() != '\n');
            printf("-> 성공적으로 수정되었습니다.\n");
            return;
        }
    }
    printf("[오류] 해당 번호의 제품을 찾을 수 없습니다.\n");
}

// 삭제(Delete) 함수
void deleteProduct()
{
    char searchId[5];
    printf("\n--- 제품 삭제 ---\n");
    printf("삭제할 제품번호(4자리) 입력 : ");
    fgets(searchId, sizeof(searchId), stdin);
    if (strchr(searchId, '\n') == NULL) while (getchar() != '\n');
    searchId[strcspn(searchId, "\n")] = '\0';

    for (int i = 0; i < productCount; i++)
    {
        if (strcmp(db[i]->id, searchId) == 0)
        {
            free(db[i]);
            for (int j = i; j < productCount - 1; j++)
            {
                db[j] = db[j + 1];
            }
            productCount--;
            printf("-> 성공적으로 삭제되었습니다.\n");
            return;
        }
    }
    printf("[오류] 해당 번호의 제품을 찾을 수 없습니다.\n");
}

// 현재 메모리에 로드된 전체 레코드 출력 함수
void printAll()
{
    printf("\n--- 현재 등록된 레코드 목록 ---\n");
    printf("id,name,qty,price,lot\n");
    for (int i = 0; i < productCount; i++)
    {
        printf("%s,%s,%d,%d,%s\n", db[i]->id, db[i]->name, db[i]->qty, db[i]->price, db[i]->lot);
    }
}

int main()
{
    loadFromFile();

    char menu;
    while (1)
    {
        printf("\n=========== 재고 관리 프로그램(V.1.00) ==========\n");
        printf("\n= [메뉴] 1.조회  2.등록  3.수정  4.삭제  5.종료 = ");
        printf("\n=================================================\n");
        scanf(" %c", &menu);
        while (getchar() != '\n'); 

        if (menu == '1') {
            printAll();
        }
        else if (menu == '2') {
            while (1) {
                insertProduct();
                char choice;
                printf("계속 입력할까요? (Y/N) : ");
                scanf(" %c", &choice); while (getchar() != '\n');
                if (choice == 'n' || choice == 'N') break;
            }
        }
        else if (menu == '3') {
            updateProduct();
        }
        else if (menu == '4') {
            deleteProduct();
        }
        else if (menu == '5') {
            saveToFile();
            printf("레코드 입력 완료 및 파일 저장 완료\n");
            break;
        }
        else {
            printf("잘못된 메뉴 선택입니다.\n");
        }
    }

    for (int i = 0; i < productCount; i++) {
        free(db[i]);
    }

    return 0;
}