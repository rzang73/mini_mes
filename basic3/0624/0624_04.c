#include <stdio.h>

int main() 
{
    FILE *fp = fopen("c.txt", "w");

    if (fp == NULL) 
    {
        printf("파일을 열 수 없습니다.\n");
        return 1; 
    }
    fprintf(fp, "Hello World~!\n");
   
    fclose(fp);
    printf("c.txt 파일에 문자열을 성공적으로 썼습니다.\n");

    return 0;
}