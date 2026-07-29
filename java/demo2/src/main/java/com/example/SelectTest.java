package com.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class SelectTest {

    public static void main(String[] args) {
        
        String url = "jdbc:sqlite:data/study.db";
        String sql = "SELECT book_id, title, author, price FROM book ORDER BY book_id";

        try(
            Connection con = DriverManager.getConnection(url);
            PreparedStatement ps = con.prepareStatement(sql);
            ResultSet rs = ps.executeQuery()
        ){
            while (rs.next()) {
        int id = rs.getInt("book_id");
        String title = rs.getString("title");
        String author = rs.getString("author");
        int price = rs.getInt("price");
        System.out.printf("%d | %s | %s | %d원%n", id, title, author, price);
    }

        }catch(Exception e){

        }

    }
}