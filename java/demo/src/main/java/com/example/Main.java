package com.example;

import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        ArrayList<String> alist = new ArrayList<String>();
        alist.add("Hello");
        alist.add("Hi");
        alist.add("Java");
        // 자료 삽입
        alist.add(2, "Shani");
        alist.remove(1);
        // 완전제거
        alist.clear();

        for(int i=0; i < alist.size(); i++){
            System.out.println(alist.get(i));
        }
    }
}