#include <stdio.h>

int main()

{
    int a,b,c,d;

    scanf("%d %d %d %d", &a, &b, &c, &d); //100,200,300,400

    //코딩
    int temp;

    temp = a;
    a = b;
    b = c;
    c = d;
    
    d = temp;
 
    printf("%d %d %d %d\n", a,b,c,d);


    return 0 ;
}

//int main()
//    int c,d;
//    scanf("%d %d", &c, &d);
//
//   int temp1;
//    temp1 = c;
//    c = d;
//    d =temp1


