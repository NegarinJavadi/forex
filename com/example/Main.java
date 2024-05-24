package com.example;

public class Main {
    public static void main(String[] args) {
        String jsonData = "{\"name\":\"John\", \"age\":30}";
        JSONObject jsonObject = new JSONObject(jsonData);
        System.out.println(jsonObject.toString());
    }
}
