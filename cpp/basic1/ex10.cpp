#include <iostream>
using namespace std;

class Calculator {
public:
    int plus(int a, int b) {
        return a + b;
    }

    int minus(int a, int b) {
        return a - b;
    }

    int multiple(int a, int b) {
        return a * b;
    }

    double divide(int a, int b) {
        if (b == 0) {
            cout << "0으로 나눌 수 없습니다." << endl;
            return 0;
        }
        return (double)a / b; 
    }
};

int main() {
    int a = 10;
    int b = 20;

    Calculator calc;

    cout << "plus결과는 : " << calc.plus(a, b) << "입니다." << endl;
    cout << "minus결과는 : " << calc.minus(a, b) << "입니다." << endl;
    cout << "multiple결과는 : " << calc.multiple(a, b) << "입니다." << endl;
    cout << "divide결과는 : " << calc.divide(a, b) << "입니다." << endl;

    return 0;
}