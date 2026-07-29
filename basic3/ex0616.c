#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define TOTAL_PARTS 20
#define STANDARD_SIZE 50.0
#define TOLERANCE 0.2

int main(void)
{
    int i;
    int ok_count = 0;
    int ng_count = 0;

    srand((unsigned int)time(NULL));

    printf("==========================================================================\n");
    printf(" 자동차 부품 스마트팩토리 검사 시스템\n");
    printf(" 기준치수: %.2f mm, 허용공차: ±%.2f mm\n", STANDARD_SIZE, TOLERANCE);
    printf(" 검사수량: %d개\n", TOTAL_PARTS);
    printf("==========================================================================\n\n");

    printf("번호\t측정치수\t표면불량\t조립불량\t판정\n");
    printf("--------------------------------------------------------------------------\n");

    for (i = 1; i <= TOTAL_PARTS; i++)
    {
        double measured_size;
        int surface_defect;
        int assembly_defect;
        int dimension_ok;

        /*
            49.70 ~ 50.30 사이의 치수를 랜덤 생성
            rand() % 61 은 0 ~ 60 사이의 정수 생성
            이것을 100.0으로 나누면 0.00 ~ 0.60
            따라서 49.70 + 0.00 ~ 0.60 = 49.70 ~ 50.30
        */
        measured_size = 49.70 + (rand() % 61) / 100.0;

        /*
            표면불량 발생 확률: 약 8%
            rand() % 100 은 0 ~ 99 사이의 숫자 발생
            그 값이 8보다 작으면 불량으로 처리
        */
        surface_defect = (rand() % 100 < 8);

        /*
            조립불량 발생 확률: 약 5%
        */
        assembly_defect = (rand() % 100 < 5);

        /*
            치수가 기준공차 안에 들어오는지 확인
            49.80 이상 50.20 이하이면 치수 OK
        */
        dimension_ok = 
            (measured_size >= STANDARD_SIZE - TOLERANCE) &&
            (measured_size <= STANDARD_SIZE + TOLERANCE);

        printf("%d\t%.2f mm\t\t%s\t\t%s\t\t",
               i,
               measured_size,
               surface_defect ? "있음" : "없음",
               assembly_defect ? "있음" : "없음");

        if (dimension_ok && surface_defect == 0 && assembly_defect == 0)
        {
            printf("OK\n");
            ok_count++;
        }
        else
        {
            printf("NG\n");
            ng_count++;
        }
    }

    printf("\n==========================================================================\n");
    printf("검사 결과 요약\n");
    printf("OK 수량 : %d개\n", ok_count);
    printf("NG 수량 : %d개\n", ng_count);
    printf("수율    : %.2f%%\n", (double)ok_count / TOTAL_PARTS * 100.0);

    if ((double)ok_count / TOTAL_PARTS * 100.0 >= 95.0)
    {
        printf("라인 상태: 양호\n");
    }
    else if ((double)ok_count / TOTAL_PARTS * 100.0 >= 85.0)
    {
        printf("라인 상태: 주의 필요\n");
    }
    else
    {
        printf("라인 상태: 즉시 점검 필요\n");
    }

    printf("==========================================================================\n");

    return 0;
}