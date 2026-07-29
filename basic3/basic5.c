#include <stdio.h>
int main()
{
   int qty;
   int total=0;
   double avg;

   for(int i=0; i<5; i++){
       scanf("%d", &qty);
       total += qty;
   }
   printf("총 생산량 : %d\n", total);
   printf("평균 생산량 : %.1lf\n", (double)total/5.0);

   return 0;
}