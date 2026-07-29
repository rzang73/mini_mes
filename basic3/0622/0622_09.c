#include <stdio.h>

int main()
{
    int score[3][4];
    int cnt = 1;

    for (int i =0; i <3; i++){
        for(int j =0; j <4; j++){
            score[i][j] = cnt++; 
          printf("%d\t", score[i][j] );
        }
     
        printf("\n");
    }
    return 0;
    }