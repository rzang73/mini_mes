#include <stdio.h>

int main()

{
    int score[5];
    int total=0;
        for (int i=0; i<5; i++)
            scanf("%d", &score[i]);           
        
 for(int i=0; i<5; i++)
        total += score[i];

 print("total : %d", total); 
    for(int i=0; i<5; i++){
        printf("%d", score[i]);
    }
printf("\n");
double avg = total /5.0;
printf("평균: %.1lf\n", avg);
    return 0;
}
