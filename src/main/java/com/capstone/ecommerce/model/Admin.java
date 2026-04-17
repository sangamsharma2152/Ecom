package com.capstone.ecommerce.model;

public class Admin extends User {
    private String adminLevel;

    public Admin(String userId, String name, String email, String password) {
        super(userId, name, email, password);
        this.adminLevel = "SUPER";
    }

    public Admin(String userId, String name, String email, String password, String adminLevel) {
        super(userId, name, email, password);
        this.adminLevel = adminLevel;
    }

    public String getAdminLevel() {
        return adminLevel;
    }

    public void setAdminLevel(String adminLevel) {
        this.adminLevel = adminLevel;
    }

    @Override    public String toCsv() {
        return userId + "," + name + "," + email + "," + password + ",ADMIN," + adminLevel;
    }

    @Override    public String toString() {
        return "Admin{" +
                "userId='" + userId + '\'' +
                ", name='" + name + '\'' +
                ", email='" + email + '\'' +
                ", adminLevel='" + adminLevel + '\'' +
                '}';
    }
}
