package com.capstone.ecommerce.util;

public final class ValidationUtil {
    private ValidationUtil() {
    }

    public static boolean isEmailValid(String email) {
        return email != null && email.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$");
    }

    public static boolean isNonEmpty(String value) {
        return value != null && !value.trim().isEmpty();
    }

    public static boolean isPositiveDouble(String number) {
        try {
            return Double.parseDouble(number) > 0;
        } catch (NumberFormatException ex) {
            return false;
        }
    }

    public static boolean isNonNegativeInt(String number) {
        try {
            return Integer.parseInt(number) >= 0;
        } catch (NumberFormatException ex) {
            return false;
        }
    }
}
