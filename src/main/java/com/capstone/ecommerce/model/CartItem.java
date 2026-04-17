package com.capstone.ecommerce.model;

public class CartItem {
    private String cartItemId;
    private Product product;
    private int quantity;

    public CartItem(Product product, int quantity) {
        this.product = product;
        this.quantity = quantity;
        this.cartItemId = product.getProductId() + "-" + System.currentTimeMillis();
    }

    public CartItem(String cartItemId, Product product, int quantity) {
        this.cartItemId = cartItemId;
        this.product = product;
        this.quantity = quantity;
    }

    public String getCartItemId() {
        return cartItemId;
    }

    public Product getProduct() {
        return product;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public double getTotalPrice() {
        return product.getPrice() * quantity;
    }

    public double getSubtotal() {
        return product.getPrice() * quantity;
    }

    @Override
    public String toString() {
        return "CartItem{" +
                "cartItemId='" + cartItemId + '\'' +
                ", product=" + product.getName() +
                ", quantity=" + quantity +
                ", totalPrice=" + getTotalPrice() +
                '}';
    }
}
