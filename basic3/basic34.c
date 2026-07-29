
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    srand(time(NULL));

    for(int i=0; i<6; i++){ 
        printf(" %d", rand()%45 +1);
    }
    printf("\n");    
    return 0;
}