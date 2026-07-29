interface Flyable {
    public void fly();

}
class Horse{
    public void run(){};
}
class Bird{
    public void fly(){};
}

class Unicon extends Horse implements Flyable{
    @Override
    public  void fly(){
        System.out.println("날다.");
    }
}

public class Flytest {
    public static void main(String[] args) {
        Unicon unicon = new Unicon();
        unicon.fly();
    }    

}
