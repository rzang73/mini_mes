#include <stdio.h>

int main()
{
    int ary1[3] = {1,2,3};
    int ary2[3] = {11,12,13};
    int ary3[3] = {21,22,23};

    int *pary[3] = {ary1,ary2,ary3};
    
    for (int i= 0 ; i<3 ; i++){
       for (int j= 0 ; j<3; j++){
            printf("%5d", pary[i][j]);
            }
        
        printf("\n");
        }
    return 0;
 }