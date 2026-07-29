class Animal {
    public String name;
    Animal(){
        this.name = "동물";
    }
    public void eat(){
        System.out.println("먹는다.");
    }
}
class Human extends Animal{
}

public class AnimalTest{
    public static void main(String[] args) {
        Human hongGilDong = new Human();
        hongGilDong.eat();
        System.out.println(hongGilDong.name);
        
    }
}