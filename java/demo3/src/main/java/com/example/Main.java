package com.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        String url = "jdbc:sqlite:data/study.db";
        String sql = "UPDATE book SET price = ? WHERE book_id = ?";

        try (Connection con = DriverManager.getConnection(url);
                PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, 13000);
            ps.setInt(2, 1);
            ps.executeUpdate();
           // System.out.println(count + "권 수정");
        } catch (Exception e) {
            System.out.println("연결 실패: " + e.getMessage());
        } // end of catch
    }// end of main
}// end of Main