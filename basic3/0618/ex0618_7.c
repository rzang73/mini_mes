#include <stdio.h>

int main()
{
    //gets(str); // 보안문제로 제거됨
    char str[80];
    fgets(str, sizeof(str), stdin);
    
    puts(str);
    
    return 0;
}