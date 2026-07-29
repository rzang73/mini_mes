#include <stdio.h>
void swap(int* p_a, int* p_b)
{
   int temp;
   temp = *p_a;
   *p_a = *p_b;
   *p_b = temp;
}

int main()
{
   int a = 10, b = 20;
   swap(&a, &b);
   printf("(a, b) : %d, %d", a, b);
   return 0;
}
