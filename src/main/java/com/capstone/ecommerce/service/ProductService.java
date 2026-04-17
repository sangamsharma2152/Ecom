package com.capstone.ecommerce.service;

import com.capstone.ecommerce.model.Product;
import com.capstone.ecommerce.util.AppConfig;
import com.capstone.ecommerce.util.FileStorageUtil;
import com.capstone.ecommerce.util.IdGenerator;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ProductService {
    private final Map<String, Product> products = new HashMap<>();

    public ProductService() {
        loadProductsFromFile();
    }

    public List<Product> getAllProducts() {
        return new ArrayList<>(products.values());
    }

    public Product getById(String productId) {
        return products.get(productId);
    }

    public List<Product> searchByName(String query) {
        List<Product> result = new ArrayList<>();
        String q = query.toLowerCase();
        for (Product product : products.values()) {
            if (product.getName().toLowerCase().contains(q)) {
                result.add(product);
            }
        }
        return result;
    }

    public List<Product> filterByCategory(String category) {
        List<Product> result = new ArrayList<>();
        for (Product product : products.values()) {
            if (product.getCategory().equalsIgnoreCase(category)) {
                result.add(product);
            }
        }
        return result;
    }

    public String addProduct(String name, double price, String category, int stock) {
        Product product = new Product(IdGenerator.generateProductId(), name, price, category, stock);
        products.put(product.getProductId(), product);
        saveProductsToFile();
        return "Product added: " + product.getProductId();
    }

    public String updateProduct(String productId, String name, double price, String category, int stock) {
        Product product = products.get(productId);
        if (product == null) {
            return "Product not found.";
        }

        product.setName(name);
        product.setPrice(price);
        product.setCategory(category);
        product.setStock(stock);
        saveProductsToFile();
        return "Product updated.";
    }

    public String deleteProduct(String productId) {
        Product removed = products.remove(productId);
        if (removed == null) {
            return "Product not found.";
        }
        saveProductsToFile();
        return "Product deleted.";
    }

    public void decreaseStock(String productId, int quantity) {
        Product product = products.get(productId);
        if (product == null) {
            return;
        }
        int newStock = product.getStock() - quantity;
        product.setStock(Math.max(newStock, 0));
        saveProductsToFile();
    }

    private void loadProductsFromFile() {
        List<String> lines = FileStorageUtil.readAllLines(AppConfig.PRODUCTS_FILE);
        for (String line : lines) {
            String[] parts = line.split(",", -1);
            if (parts.length != 5) {
                continue;
            }
            try {
                Product product = new Product(
                        parts[0],
                        parts[1],
                        Double.parseDouble(parts[2]),
                        parts[3],
                        Integer.parseInt(parts[4])
                );
                products.put(product.getProductId(), product);
            } catch (NumberFormatException ignored) {
            }
        }
    }

    private void saveProductsToFile() {
        List<String> lines = new ArrayList<>();
        for (Product product : products.values()) {
            lines.add(product.toCsv());
        }
        FileStorageUtil.writeAllLines(AppConfig.PRODUCTS_FILE, lines);
    }
}
