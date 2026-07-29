#include <stdio.h>

int main()
{
   int array[7] ={4,5,8,1,2,3,7};
   int min = array[0] ;

   for (int i = 0; i < 7; i++){
        if ( min > array[i] ){
            min = array[i]; 
        }
    }
   printf("min = %d\n", min);

    return 0;
}