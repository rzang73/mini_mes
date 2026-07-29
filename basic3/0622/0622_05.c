#include <stdio.h>
#include <string.h>
int main()
{
    char str1[80] = "pear";
    char str2[80] = "pear";

    if(strcmp(str1, str2) == 0)
        printf("두 문자열이 같다,\n");
    return 0;
}