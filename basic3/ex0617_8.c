#include <stdio.h>
void fruit(int count)
{
    printf("%d : apple\n", count);
        if(count==5) return;
        fruit(count +1);
}

int main()
{
    fruit(1);
    return 0;
}