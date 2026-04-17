# E-Commerce Management System (Phase 1)

This version is prepared only for the first evaluation (Unit 3 scope):
- Classes and objects
- Inheritance and abstraction
- Static members
- File handling
- Multithreading
- Collections

## 1. Folder Structure (Phase 1)

```text
Capstone project/
├─ src/
│  └─ com/capstone/ecommerce/
│     ├─ app/
│     │  └─ AppMain.java
│     ├─ model/
│     │  ├─ User.java
│     │  ├─ Customer.java
│     │  ├─ Admin.java
│     │  ├─ Product.java
│     │  ├─ CartItem.java
│     │  ├─ Order.java
│     │  └─ OrderStatus.java
│     ├─ service/
│     │  ├─ AuthService.java
│     │  ├─ ProductService.java
│     │  ├─ CartService.java
│     │  ├─ OrderService.java
│     │  └─ OrderProcessingThread.java
│     └─ util/
│        ├─ AppConfig.java
│        ├─ FileStorageUtil.java
│        ├─ ValidationUtil.java
│        └─ IdGenerator.java
├─ data/
│  ├─ users.csv
│  ├─ products.csv
│  └─ orders.csv
└─ README.md
```

## 2. Implemented Requirements

### User Management
- Abstract class `User`
- Subclasses `Admin` and `Customer`
- Register and login flow
- Role-based behavior in console menus

### Product Management
- Admin can add, update, delete, list products
- Product fields: ID, Name, Price, Category, Stock

### Cart and Order
- Customer can add/remove items from cart
- Total amount calculation
- Order placement and order history

### File Handling
- Users, products, and orders are persisted in CSV files
- Read and write operations are centralized in `FileStorageUtil`

### Multithreading
- `OrderProcessingThread` simulates background processing
- Order status changes from `PENDING` to `PROCESSING` to `CONFIRMED`

### Collections
- `ArrayList` for product/order/cart lists
- `HashMap` for fast lookup in services

## 3. How To Run

From project root:

```powershell
if (!(Test-Path out)) { New-Item -ItemType Directory -Path out | Out-Null }
$files = Get-ChildItem -Path src -Filter *.java -Recurse | ForEach-Object { $_.FullName }
javac -d out $files
java -cp out com.capstone.ecommerce.app.AppMain
```

Default admin login:
- Email: `admin@shop.com`
- Password: `admin123`

Sample customer login:
- Email: `alice@mail.com`
- Password: `alice123`

## 4. Viva Notes

- **Abstraction**: `User` is abstract and shared by all user types.
- **Inheritance**: `Admin` and `Customer` extend `User`.
- **Static**: `User.getTotalUsers()` demonstrates static state.
- **File handling**: CSV files in `data/` store all persistent records.
- **Multithreading**: order confirmation runs in background thread.
- **Validation and exception handling**: numeric and email checks, guarded parsing.

## 5. Scope Statement

This repository is intentionally trimmed to Phase 1 only.
GUI and database connectivity are excluded in this submission branch/version.
