package com.capstone.ecommerce.service;

import com.capstone.ecommerce.model.CartItem;
import com.capstone.ecommerce.model.Product;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CartService {
    private final Map<String, CartItem> cartMap = new HashMap<>();

    public String addToCart(Product product, int quantity) {
        if (quantity <= 0) {
            return "Quantity must be positive.";
        }
        if (product.getStock() < quantity) {
            return "Insufficient stock.";
        }

        CartItem existing = cartMap.get(product.getProductId());
        int finalQty = quantity;
        if (existing != null) {
            finalQty += existing.getQuantity();
        }

        if (finalQty > product.getStock()) {
            return "Total cart quantity exceeds stock.";
        }

        cartMap.put(product.getProductId(), new CartItem(product, finalQty));
        return "Added to cart.";
    }

    public String removeFromCart(String productId) {
        if (cartMap.remove(productId) == null) {
            return "Item not in cart.";
        }
        return "Removed from cart.";
    }

    public List<CartItem> getItems() {
        return new ArrayList<>(cartMap.values());
    }

    public boolean isEmpty() {
        return cartMap.isEmpty();
    }

    public double getTotal() {
        double total = 0;
        for (CartItem item : cartMap.values()) {
            total += item.getSubtotal();
        }
        return total;
    }

    public void clear() {
        cartMap.clear();
    }
}
