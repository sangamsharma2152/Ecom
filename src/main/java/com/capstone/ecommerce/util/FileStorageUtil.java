package com.capstone.ecommerce.util;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public final class FileStorageUtil {
    private FileStorageUtil() {
    }

    public static List<String> readAllLines(String filePath) {
        List<String> lines = new ArrayList<>();
        File file = new File(filePath);
        if (!file.exists()) {
            return lines;
        }

        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (!line.trim().isEmpty()) {
                    lines.add(line);
                }
            }
        } catch (IOException ex) {
            throw new RuntimeException("Failed to read file: " + filePath, ex);
        }
        return lines;
    }

    public static void writeAllLines(String filePath, List<String> lines) {
        ensureParentDir(filePath);
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
            for (String line : lines) {
                writer.write(line);
                writer.newLine();
            }
        } catch (IOException ex) {
            throw new RuntimeException("Failed to write file: " + filePath, ex);
        }
    }

    public static void appendLine(String filePath, String line) {
        ensureParentDir(filePath);
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath, true))) {
            writer.write(line);
            writer.newLine();
        } catch (IOException ex) {
            throw new RuntimeException("Failed to append file: " + filePath, ex);
        }
    }

    private static void ensureParentDir(String filePath) {
        File file = new File(filePath);
        File parent = file.getParentFile();
        if (parent != null && !parent.exists()) {
            parent.mkdirs();
        }
    }
}
