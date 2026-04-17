package com.capstone.ecommerce.model;

public class Customer extends User {
    private String address;

    public Customer(String userId, String name, String email, String password, String address) {
        super(userId, name, email, password);
        this.address = address;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    @Override    public String toCsv() {
        return userId + "," + name + "," + email + "," + password + ",CUSTOMER," + address;
    }

    @Override    public String toString() {
        return "Customer{" +
                "userId='" + userId + '\'' +
                ", name='" + name + '\'' +
                ", email='" + email + '\'' +
                ", address='" + address + '\'' +
                '}';
    }
}
