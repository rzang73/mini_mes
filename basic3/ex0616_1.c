#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define TOTAL_PARTS 50

#define STANDARD_SIZE 50.0
#define TOLERANCE 0.2

#define USL (STANDARD_SIZE + TOLERANCE)
#define LSL (STANDARD_SIZE - TOLERANCE)

int main(void)
{
    int i;
    int ok_count = 0;
    int ng_count = 0;

    double data[TOTAL_PARTS];

    double sum = 0.0;
    double average = 0.0;
    double variance = 0.0;
    double std_dev = 0.0;

    double max_value;
    double min_value;

    double cp = 0.0;
    double cpk = 0.0;
    double cpu = 0.0;
    double cpl = 0.0;

    srand((unsigned int)time(NULL));

    printf("============================================\n");
    printf(" 자동차 부품 스마트팩토리 치수 검사 시스템\n");
    printf(" 기준치수 : %.2f mm\n", STANDARD_SIZE);
    printf(" 상한규격 USL : %.2f mm\n", USL);
    printf(" 하한규격 LSL : %.2f mm\n", LSL);
    printf(" 검사수량 : %d개\n", TOTAL_PARTS);
    printf("============================================\n\n");

    printf("번호\t측정치수\t판정\n");
    printf("--------------------------------------------\n");

    for (i = 0; i < TOTAL_PARTS; i++)
    {
        /*
            49.70 ~ 50.30 사이의 치수 데이터를 랜덤 생성
            실제 현장에서는 센서, 비전검사기, 3차원 측정기 데이터에 해당
        */
        data[i] = 49.70 + (rand() % 61) / 100.0;

        sum += data[i];

        if (i == 0)
        {
            max_value = data[i];
            min_value = data[i];
        }
        else
        {
            if (data[i] > max_value)
            {
                max_value = data[i];
            }

            if (data[i] < min_value)
            {
                min_value = data[i];
            }
        }

        printf("%d\t%.2f mm\t\t", i + 1, data[i]);

        if (data[i] >= LSL && data[i] <= USL)
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

    average = sum / TOTAL_PARTS;

    /*
        표준편차 계산
        여기서는 표본 표준편차를 사용
        분모를 TOTAL_PARTS - 1 로 계산
    */
    for (i = 0; i < TOTAL_PARTS; i++)
    {
        variance += pow(data[i] - average, 2);
    }

    variance = variance / (TOTAL_PARTS - 1);
    std_dev = sqrt(variance);

    /*
        Cp 계산식
        Cp = (USL - LSL) / (6 * 표준편차)

        Cpk 계산식
        Cpu = (USL - 평균) / (3 * 표준편차)
        Cpl = (평균 - LSL) / (3 * 표준편차)
        Cpk = Cpu와 Cpl 중 작은 값
    */
    if (std_dev > 0)
    {
        cp = (USL - LSL) / (6 * std_dev);

        cpu = (USL - average) / (3 * std_dev);
        cpl = (average - LSL) / (3 * std_dev);

        if (cpu < cpl)
        {
            cpk = cpu;
        }
        else
        {
            cpk = cpl;
        }
    }

    printf("\n============================================\n");
    printf("검사 결과 요약\n");
    printf("============================================\n");
    printf("검사 수량       : %d개\n", TOTAL_PARTS);
    printf("OK 수량         : %d개\n", ok_count);
    printf("NG 수량         : %d개\n", ng_count);
    printf("수율            : %.2f %%\n", (double)ok_count / TOTAL_PARTS * 100.0);

    printf("--------------------------------------------\n");
    printf("평균값          : %.4f mm\n", average);
    printf("표준편차        : %.4f mm\n", std_dev);
    printf("최대값          : %.4f mm\n", max_value);
    printf("최소값          : %.4f mm\n", min_value);

    printf("--------------------------------------------\n");
    printf("Cp              : %.4f\n", cp);
    printf("Cpu             : %.4f\n", cpu);
    printf("Cpl             : %.4f\n", cpl);
    printf("Cpk             : %.4f\n", cpk);

    printf("--------------------------------------------\n");

    if (cp >= 1.67 && cpk >= 1.67)
    {
        printf("공정능력 판정   : 매우 우수\n");
    }
    else if (cp >= 1.33 && cpk >= 1.33)
    {
        printf("공정능력 판정   : 양호\n");
    }
    else if (cp >= 1.00 && cpk >= 1.00)
    {
        printf("공정능력 판정   : 보통, 관리 필요\n");
    }
    else
    {
        printf("공정능력 판정   : 부족, 개선 필요\n");
    }

    printf("============================================\n");

    return 0;
}