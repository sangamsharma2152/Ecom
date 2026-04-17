package com.capstone.ecommerce.model;

public class Product {
    private String productId;
    private String name;
    private double price;
    private String category;
    private int stock;

    public Product(String productId, String name, double price, String category, int stock) {
        this.productId = productId;
        this.name = name;
        this.price = price;
        this.category = category;
        this.stock = stock;
    }

    public String getProductId() {
        return productId;
    }

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }

    public int getStock() {
        return stock;
    }

    public void setStock(int stock) {
        this.stock = stock;
    }

    public String getCategory() {
        return category;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String toCsv() {
        return productId + "," + name + "," + price + "," + category + "," + stock;
    }

    @Override
    public String toString() {
        return "Product{" +
                "productId='" + productId + '\'' +
                ", name='" + name + '\'' +
                ", price=" + price +
                ", category='" + category + '\'' +
                ", stock=" + stock +
                '}';
    }
}
