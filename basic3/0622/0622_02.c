#include <stdio.h>

int main()
{
    char str[80];

    scanf("%s", str); //apple jam
    printf("%s \n", str); //apple
    
    scanf("%s", str); //buffer --> jam
    printf("%s\n", str); // jam
    
    return 0;
}