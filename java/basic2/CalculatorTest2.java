
class Calculator2{
    public int plus(int a, int b){
        return a + b;
    }

    public int plus(int a, int b, int c){
        return a + b + c;
    }

}

public class CalculatorTest2{
    public static void main(String[] args) {
        Calculator2 cal2 = new Calculator2();
            System.out.println(cal2.plus(3, 7));
            System.out.println(cal2.plus(3, 7));
            System.out.println(cal2.plus(3, 7));
    }

}