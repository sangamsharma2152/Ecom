package com.capstone.ecommerce.service;

import com.capstone.ecommerce.model.Admin;
import com.capstone.ecommerce.model.Customer;
import com.capstone.ecommerce.model.User;
import com.capstone.ecommerce.util.AppConfig;
import com.capstone.ecommerce.util.FileStorageUtil;
import com.capstone.ecommerce.util.IdGenerator;
import com.capstone.ecommerce.util.ValidationUtil;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class AuthService {
    private final Map<String, User> usersByEmail = new HashMap<>();

    public AuthService() {
        loadUsersFromFile();
        ensureDefaultAdmin();
    }

    public User login(String email, String password) {
        User user = usersByEmail.get(email.toLowerCase());
        if (user == null || !user.passwordMatches(password)) {
            return null;
        }
        return user;
    }

    public String registerCustomer(String name, String email, String password, String address) {
        if (!ValidationUtil.isNonEmpty(name) || !ValidationUtil.isNonEmpty(password) || !ValidationUtil.isNonEmpty(address)) {
            return "Name, password, and address cannot be empty.";
        }
        if (!ValidationUtil.isEmailValid(email)) {
            return "Invalid email format.";
        }

        String key = email.toLowerCase();
        if (usersByEmail.containsKey(key)) {
            return "Email already registered.";
        }

        Customer customer = new Customer(IdGenerator.generateUserId(), name, key, password, address);
        usersByEmail.put(key, customer);
        saveUsersToFile();

        return "Registration successful.";
    }

    public List<User> getAllUsers() {
        return new ArrayList<>(usersByEmail.values());
    }

    private void ensureDefaultAdmin() {
        if (!usersByEmail.containsKey("admin@shop.com")) {
            Admin admin = new Admin("A-0001", "System Admin", "admin@shop.com", "admin123");
            usersByEmail.put(admin.getEmail().toLowerCase(), admin);
            saveUsersToFile();
        }
    }

    private void loadUsersFromFile() {
        List<String> lines = FileStorageUtil.readAllLines(AppConfig.USERS_FILE);
        for (String line : lines) {
            String[] parts = line.split(",", -1);
            if (parts.length < 5) {
                continue;
            }

            String userId = parts[0];
            String name = parts[1];
            String email = parts[2].toLowerCase();
            String password = parts[3];
            String role = parts[4];

            if ("ADMIN".equalsIgnoreCase(role)) {
                usersByEmail.put(email, new Admin(userId, name, email, password));
            } else {
                StringBuilder addressBuilder = new StringBuilder();
                for (int i = 5; i < parts.length; i++) {
                    if (addressBuilder.length() > 0) {
                        addressBuilder.append(",");
                    }
                    addressBuilder.append(parts[i]);
                }
                String address = addressBuilder.length() > 0 ? addressBuilder.toString() : "N/A";
                usersByEmail.put(email, new Customer(userId, name, email, password, address));
            }
        }
    }

    private void saveUsersToFile() {
        List<String> lines = new ArrayList<>();
        for (User user : usersByEmail.values()) {
            lines.add(user.toCsv());
        }
        FileStorageUtil.writeAllLines(AppConfig.USERS_FILE, lines);
    }
}
