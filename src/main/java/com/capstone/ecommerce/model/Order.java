package com.capstone.ecommerce.model;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class Order {
    private String orderId;
    private String customerId;
    private List<CartItem> items;
    private OrderStatus status;
    private double totalAmount;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private String shippingAddress;

    public Order(String orderId, String customerId, List<CartItem> items, String shippingAddress) {
        this.orderId = orderId;
        this.customerId = customerId;
        this.items = new ArrayList<>(items);
        this.status = OrderStatus.PENDING;
        this.shippingAddress = shippingAddress;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
        calculateTotal();
    }

    public Order(String orderId, String customerId, List<CartItem> items, LocalDateTime createdAt, OrderStatus status) {
        this.orderId = orderId;
        this.customerId = customerId;
        this.items = new ArrayList<>(items);
        this.status = status;
        this.createdAt = createdAt;
        this.updatedAt = LocalDateTime.now();
        this.shippingAddress = "";
        calculateTotal();
    }

    private void calculateTotal() {
        this.totalAmount = items.stream().mapToDouble(CartItem::getTotalPrice).sum();
    }

    public String getOrderId() {
        return orderId;
    }

    public String getCustomerId() {
        return customerId;
    }

    public List<CartItem> getItems() {
        return new ArrayList<>(items);
    }

    public OrderStatus getStatus() {
        return status;
    }

    public void setStatus(OrderStatus status) {
        this.status = status;
        this.updatedAt = LocalDateTime.now();
    }

    public double getTotalAmount() {
        return totalAmount;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public String getShippingAddress() {
        return shippingAddress;
    }
    public String toCsv() {
        StringBuilder sb = new StringBuilder();
        sb.append(orderId).append(",").append(customerId).append(",");
        sb.append(status).append(",").append(totalAmount).append(",");
        sb.append(createdAt).append(",").append(shippingAddress);
        return sb.toString();
    }
    @Override
    public String toString() {
        return "Order{" +
                "orderId='" + orderId + '\'' +
                ", customerId='" + customerId + '\'' +
                ", status=" + status +
                ", totalAmount=" + totalAmount +
                ", createdAt=" + createdAt +
                '}';
    }
}
