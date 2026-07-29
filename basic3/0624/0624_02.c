#include <stdio.h>

void calculateGCDandLCM(int a, int b, int *gcdPtr, long long *lcmPtr) 
{
    int originalA = a;
    int originalB = b;
    
    while (b != 0) 
    {
        int remainder = a % b;
        a = b;
        b = remainder;
    }
    *gcdPtr = a; 

    *lcmPtr = ((long long)originalA * originalB) / (*gcdPtr);
}

int main() 
{
    int num1, num2;
    int gcd = 0;
    long long lcm = 0; 

    if (scanf("%d %d", &num1, &num2) != 2) 
    {
        return 1;
    }

    calculateGCDandLCM(num1, num2, &gcd, &lcm);

    printf(" 최대공약수:%d\n 최소공배수:%lld\n", gcd, lcm);

    return 0;
}