#include <stdio.h>

void swap(int *x, int *y)
{
    int temp;

    temp = *x;
    *x = *y;
    *y = temp;
}

int main()
{
    int a = 10, b = 20;

    int x_before = a;
    int y_before = b;

    printf("(a, b): %d, %d\n", a, b);

    swap(&a, &b);

    printf("(a, b): %d, %d\n", a, b);

    printf("(x, y): %d, %d\n", x_before, y_before);
    printf("(x, y): %d, %d\n", a, b);

    return 0;
}
