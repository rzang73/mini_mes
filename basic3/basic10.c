#include <stdio.h>

int main()
{
for(int i=9; i>=2; i--){

       for(int j=9; j>=2; j--){
           printf("%d * %d = %d\n", i, j, i * j);
       }

       printf("\n");
   }

   return 0;
}