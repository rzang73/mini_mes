#include <stdio.h>

int main() 
{
    print_big();
    print_small();
    print_number();

    return 0;
}


void print_big()
{
    char ch;
    for (ch = 'A'; ch <= 'Z'; ch++)
    {
        printf("%c ", ch);
    }
    printf("\n"); 
}


void print_small()
{
    char ch;
    for (ch = 'a'; ch <= 'z'; ch++)
    {
        printf("%c ", ch);
    }
    printf("\n"); 
}

void print_number()
{
    int i;
    for (i = 0; i <= 9; i++)
    {
        printf("%d ", i);
    }
    printf("\n"); 
}

