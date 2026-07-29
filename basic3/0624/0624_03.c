#include <stdio.h>

int main()
{
    FILE *fp;
    char str[] = "banana";
    fp = fopen(b.txt, "w");

    int i = 0;
    while(str[i] != '\0') {
        fputc(str[i], fp);
        printf("%c", str[i]);
        i++;
    }
    fputc('\n');

    return 0;
}