#include <stdio.h>

int main()
{
    char ch;
    int i;

    for(i = 0; i < 3; i++)
    {
        scanf("%c", &ch);
        printf("%c", ch);
    }
    printf("\n");
    return 0;
}