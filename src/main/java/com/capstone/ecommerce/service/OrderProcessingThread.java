package com.capstone.ecommerce.service;

import com.capstone.ecommerce.model.Order;
import com.capstone.ecommerce.model.OrderStatus;

public class OrderProcessingThread extends Thread {
    public interface OrderCallback {
        void onProcessed(Order order);
    }

    private final Order order;
    private final OrderCallback callback;

    public OrderProcessingThread(Order order, OrderCallback callback) {
        this.order = order;
        this.callback = callback;
    }

    @Override
    public void run() {
        try {
            order.setStatus(OrderStatus.PROCESSING);
            Thread.sleep(2000);
            order.setStatus(OrderStatus.CONFIRMED);
            callback.onProcessed(order);
        } catch (InterruptedException ex) {
            Thread.currentThread().interrupt();
        }
    }
}
