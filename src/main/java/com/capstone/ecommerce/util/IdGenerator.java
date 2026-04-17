package com.capstone.ecommerce.util;

import java.util.UUID;

public final class IdGenerator {
    private IdGenerator() {
    }

    public static String generateUserId() {
        return "U-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    }

    public static String generateProductId() {
        return "P-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    }

    public static String generateOrderId() {
        return "O-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    }
}
