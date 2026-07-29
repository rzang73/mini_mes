class Person{
    private int weight;
        
    public void getWeight(int weight){
        this.weight =weight;
    }

    public int getWeight(){
        return weight;
    }

}

class Student extends Person{

}

public class InheritanceEx {
    public static void main(String[] args) {
        Student gildong = new Student();
    
        gildong.getWeight(70);
        System.out.println("길동의 몸무게는 " + gildong.getWeight() + "kg입니다");            
   }
}
