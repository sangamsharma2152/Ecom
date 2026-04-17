package com.capstone.ecommerce.service;

import com.capstone.ecommerce.model.CartItem;
import com.capstone.ecommerce.model.Order;
import com.capstone.ecommerce.model.OrderStatus;
import com.capstone.ecommerce.model.Product;
import com.capstone.ecommerce.util.AppConfig;
import com.capstone.ecommerce.util.FileStorageUtil;
import com.capstone.ecommerce.util.IdGenerator;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class OrderService {
    private final Map<String, List<Order>> ordersByCustomer = new HashMap<>();
    private final ProductService productService;

    public OrderService(ProductService productService) {
        this.productService = productService;
        loadOrdersFromFile();
    }

    public String placeOrder(String customerId, List<CartItem> items, Runnable onOrderConfirmed) {
        if (items == null || items.isEmpty()) {
            return "Cart is empty.";
        }

        Order order = new Order(
                IdGenerator.generateOrderId(),
                customerId,
                items,
                LocalDateTime.now(),
                OrderStatus.PENDING
        );

        ordersByCustomer.computeIfAbsent(customerId, k -> new ArrayList<>()).add(order);

        for (CartItem item : items) {
            productService.decreaseStock(item.getProduct().getProductId(), item.getQuantity());
        }

        saveOrdersToFile();

        // Background simulation for processing and confirmation.
        OrderProcessingThread processingThread = new OrderProcessingThread(order, processed -> {
            saveOrdersToFile();
            if (onOrderConfirmed != null) {
                onOrderConfirmed.run();
            }
        });
        processingThread.start();

        return "Order placed successfully. Order ID: " + order.getOrderId();
    }

    public List<Order> getOrdersByCustomer(String customerId) {
        return ordersByCustomer.getOrDefault(customerId, new ArrayList<>());
    }

    private void loadOrdersFromFile() {
        List<String> lines = FileStorageUtil.readAllLines(AppConfig.ORDERS_FILE);
        for (String line : lines) {
            String[] parts = line.split(",", 5);
            if (parts.length < 5) {
                continue;
            }

            try {
                String orderId = parts[0];
                String customerId = parts[1];
                LocalDateTime orderTime = LocalDateTime.parse(parts[2]);
                OrderStatus status = OrderStatus.valueOf(parts[3]);

                List<CartItem> parsedItems = new ArrayList<>();
                if (!parts[4].trim().isEmpty()) {
                    String[] itemEntries = parts[4].split("\\|");
                    for (String entry : itemEntries) {
                        String[] itemParts = entry.split(":", 2);
                        if (itemParts.length != 2) {
                            continue;
                        }

                        Product product = productService.getById(itemParts[0]);
                        if (product == null) {
                            continue;
                        }

                        int quantity = Integer.parseInt(itemParts[1]);
                        parsedItems.add(new CartItem(product, quantity));
                    }
                }

                Order order = new Order(orderId, customerId, parsedItems, orderTime, status);
                ordersByCustomer.computeIfAbsent(customerId, k -> new ArrayList<>()).add(order);
            } catch (Exception ignored) {
            }
        }
    }

    private void saveOrdersToFile() {
        List<String> lines = new ArrayList<>();
        for (List<Order> customerOrders : ordersByCustomer.values()) {
            for (Order order : customerOrders) {
                lines.add(order.toCsv());
            }
        }
        FileStorageUtil.writeAllLines(AppConfig.ORDERS_FILE, lines);
    }
}
