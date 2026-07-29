package com.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Main {
    public static void main(String[] args) {
        String url = "jdbc:sqlite:data/study.db";
        try (Connection connection = DriverManager.getConnection(url)) {
            System.out.println("데이터베이스 연결 성공");
        } catch (SQLException e) {
            System.out.println("연결 실패: " + e.getMessage());
        }
    }
}