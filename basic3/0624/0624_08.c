#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#if defined(_WIN32) || defined(_WIN64)
    #include <windows.h>
#else
    #include <unistd.h>
    #include <libgen.h>
#endif

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

// 실행 파일과 동일한 폴더의 절대 경로를 구하는 함수
void getFullPath(char *filename, char *outPath)
{
    char exePath[260] = {0};
#if defined(_WIN32) || defined(_WIN64)
    GetModuleFileNameA(NULL, exePath, sizeof(exePath));
    char *lastSlash = strrchr(exePath, '\\');
    if (lastSlash != NULL) *(lastSlash + 1) = '\0';
#else
    int len = readlink("/proc/self/exe", exePath, sizeof(exePath) - 1);
    if (len != -1) {
        exePath[len] = '\0';
        char *lastSlash = strrchr(exePath, '/');
        if (lastSlash != NULL) *(lastSlash + 1) = '\0';
    }
#endif
    sprintf(outPath, "%s%s", exePath, filename);
}

// 1. 파일 로드 기능 (같은 폴더 절대 경로 적용)
void loadFromFile()
{
    char fullPath[300];
    getFullPath("products.txt", fullPath); // 절대 경로 획득

    FILE *fp = fopen(fullPath, "r");
    if (fp == NULL) {
        printf("[안내] %s 파일을 찾을 수 없어 새로 시작합니다.\n", fullPath);
        return; 
    }

    char line[250];
    productCount = 0; 

    while (fgets(line, sizeof(line), fp) != NULL && productCount < MAX_PRODUCTS)
    {
        line[strcspn(line, "\r\n")] = '\0';

        if (strlen(line) == 0 || strstr(line, "id") != NULL) {
            continue;
        }

        char *token = strtok(line, ",");
        if (token == NULL) continue;
        char tempId[10]; strcpy(tempId, token);

        token = strtok(NULL, ",");
        if (token == NULL) continue;
        char tempName[50]; strcpy(tempName, token);

        token = strtok(NULL, ",");
        if (token == NULL) continue;
        int tempQty = atoi(token);

        token = strtok(NULL, ",");
        if (token == NULL) continue;
        int tempPrice = atoi(token);

        token = strtok(NULL, ",");
        if (token == NULL) continue;
        char tempLot[30]; strcpy(tempLot, token);

        Product *p = (Product*)malloc(sizeof(Product));
        strcpy(p->id, tempId);
        strcpy(p->name, tempName);
        p->qty = tempQty;
        p->price = tempPrice;
        strcpy(p->lot, tempLot);

        db[productCount++] = p;
    }
    fclose(fp);
    printf("[완료] %d개의 레코드를 '%s'에서 정상적으로 불러왔습니다.\n", productCount, fullPath);
}

// 2. 파일 저장 기능 (같은 폴더 절대 경로 적용)
void saveToFile()
{
    if (productCount == 0)
    {
        printf("[안내] 저장할 레코드가 없어 products.txt를 덮어쓰지 않습니다.\n");
        return;
    }
    char fullPath[300];
    getFullPath("products.txt", fullPath);

    FILE *fp = fopen(fullPath, "w+");
    if (fp == NULL)
    {
        printf("파일을 저장할 수 없습니다.\n");
        return;
    }

    fseek(fp, 0, SEEK_SET);
    fprintf(fp, "id,name,qty,price,lot\n");

    for (int i = 0; i < productCount; i++)
    {
        fprintf(fp, "%s,%s,%d,%d,%s\n", db[i]->id, db[i]->name, db[i]->qty, db[i]->price, db[i]->lot);
    }
    fclose(fp);
}

int checkDuplicate(const char *searchId, const char *searchName)
{
    for (int i = 0; i < productCount; i++)
    {
        if (strcmp(db[i]->id, searchId) == 0) return 1;
        if (strcmp(db[i]->name, searchName) == 0) return 2;
    }
    return 0;
}

int findProductByName(const char *name)
{
    for (int i = 0; i < productCount; i++)
    {
        if (strcmp(db[i]->name, name) == 0)
        {
            return i;
        }
    }
    return -1;
}

// 3. 등록 기능
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

    printf("-> 메모리에 추가 완료!\n");
}

// 4. 정보 수정 기능
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

// 5. 삭제 기능
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

// 6. 출고 기능 (같은 폴더 절대 경로 적용)
void releaseProduct()
{
    char date[20];
    char name[50];
    int reqQty;
    int foundIndex;

    printf("\n--- 제품 출고 등록 ---\n");
    printf("출고일자 입력 (8자리, 예: 20260624) : ");
    fgets(date, sizeof(date), stdin);
    if (strchr(date, '\n') == NULL) while (getchar() != '\n');
    date[strcspn(date, "\n")] = '\0';

    printf("출고 품목명 입력 : ");
    fgets(name, sizeof(name), stdin);
    if (strchr(name, '\n') == NULL) while (getchar() != '\n');
    name[strcspn(name, "\n")] = '\0';

    foundIndex = findProductByName(name);
    if (foundIndex == -1)
    {
        printf("[오류] 등록되지 않은 품목명입니다.\n");
        return;
    }

    printf("출고 수량 입력 : ");
    scanf("%d", &reqQty); while (getchar() != '\n');

    if (reqQty <= 0)
    {
        printf("[오류] 출고 수량은 1개 이상이어야 합니다.\n");
        return;
    }

    if (db[foundIndex]->qty < reqQty)
    {
        printf("[오류] 재고가 부족합니다. (현재 재고: %d개)\n", db[foundIndex]->qty);
        return;
    }

    int price = db[foundIndex]->price;
    int totalPrice = reqQty * price;
    db[foundIndex]->qty -= reqQty;

    char filename[80];
    sprintf(filename, "출고일자(%s).txt", date);

    char fullLogPath[300];
    getFullPath(filename, fullLogPath);

    int totalSum = 0;
    FILE *fpRead = fopen(fullLogPath, "r");
    char fileLines[100][200];
    int lineIdx = 0;

    if (fpRead != NULL)
    {
        while (lineIdx < 100 && fgets(fileLines[lineIdx], sizeof(fileLines[lineIdx]), fpRead) != NULL)
        {
            char lineCopy[200];
            char *token;
            char *lastToken = NULL;

            strcpy(lineCopy, fileLines[lineIdx]);
            lineCopy[strcspn(lineCopy, "\r\n")] = '\0';

            if (strlen(lineCopy) == 0 || strstr(lineCopy, "합산금액") != NULL)
            {
                continue;
            }

            token = strtok(lineCopy, ",");
            while (token != NULL)
            {
                lastToken = token;
                token = strtok(NULL, ",");
            }

            if (lastToken != NULL && strstr(fileLines[lineIdx], "날짜") == NULL)
            {
                totalSum += atoi(lastToken);
            }

            lineIdx++;
        }
        fclose(fpRead);
    }

    totalSum += totalPrice;

    FILE *fpWrite = fopen(fullLogPath, "w");
    if (fpWrite == NULL)
    {
        db[foundIndex]->qty += reqQty;
        printf("출고일자 파일을 생성할 수 없습니다.\n");
        return;
    }

    if (lineIdx == 0)
    {
        fprintf(fpWrite, "날짜,품목,수량,단가,총액\n");
    }

    for (int i = 0; i < lineIdx; i++)
    {
        fprintf(fpWrite, "%s", fileLines[i]);
        if (strlen(fileLines[i]) > 0 && fileLines[i][strlen(fileLines[i]) - 1] != '\n') fprintf(fpWrite, "\n");
    }

    fprintf(fpWrite, "%s,%s,%d,%d,%d\n", date, name, reqQty, price, totalPrice);
    fprintf(fpWrite, "합산금액,,,,%d\n", totalSum);
    fclose(fpWrite);

    saveToFile();

    printf("-> 출고 완료! 재고가 %d개로 차감되었고 '%s' 파일에 기록했습니다.\n", db[foundIndex]->qty, fullLogPath);
}
// 7. 조회 기능
void printAll()
{
    printf("\n--- 현재 등록된 레코드 목록 ---\n");
    printf("id,name,qty,price,lot\n");
    if (productCount == 0) {
        printf("(경고: 등록된 데이터가 없습니다. 실행 파일이 위치한 폴더에 'products.txt'가 존재하는지 검사하세요.)\n");
        return;
    }
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
        printf("\n================ 재고 관리 프로그램(V.1.00) =============\n");
        printf("\n=                                                       = ");
        printf("\n= [메뉴] 1.조회  2.등록  3.수정  4.삭제  5.출고  6.종료 = ");
        printf("\n=                                                       =");
        printf("\n=========================================================\n");
        scanf(" %c", &menu);
        while (getchar() != '\n');

        switch (menu)
        {
            case '1':
                printAll();
                break;

            case '2':
                while (1)
                {
                    insertProduct();
                    char choice;
                    printf("계속 입력할까요? (Y/N) : ");
                    scanf(" %c", &choice);
                    while (getchar() != '\n');
                    if (choice == 'n' || choice == 'N') break;
                }
                break;

            case '3':
                updateProduct();
                break;

            case '4':
                deleteProduct();
                break;

            case '5':
                releaseProduct();
                break;

            case '6':
                saveToFile();
                printf("레코드 입력 완료 및 파일 저장 완료\n");
                for (int i = 0; i < productCount; i++)
                {
                    free(db[i]);
                }
                return 0;

            default:
                printf("잘못된 메뉴 선택입니다.\n");
                break;
        }

    }
}