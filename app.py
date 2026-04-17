import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

# Page config
st.set_page_config(
    page_title="E-Commerce Management System",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .product-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem;
    }
    .price-tag {
        font-size: 1.5rem;
        color: #2ecc71;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_role' not in st.session_state:
    st.session_state.user_role = "CUSTOMER"  # Default to customer
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'user_email' not in st.session_state:
    st.session_state.user_email = "demo@user.com"

# Load data files
def load_csv_data(filename):
    """Load data from CSV files"""
    data_dir = Path("deployment/data")
    file_path = data_dir / filename
    
    if not file_path.exists():
        return []
    
    try:
        if filename == "products.csv":
            df = pd.read_csv(file_path, names=["product_id", "name", "price", "category", "stock"])
            return df.to_dict('records')
        elif filename == "users.csv":
            df = pd.read_csv(file_path, names=["user_id", "name", "email", "password", "role", "extra"])
            return df.to_dict('records')
        elif filename == "orders.csv":
            df = pd.read_csv(file_path, names=["order_id", "customer_id", "status", "total", "date", "address"])
            return df.to_dict('records')
    except:
        pass
    
    return []

# Authentication functions
def authenticate_user(email, password):
    """Authenticate user against user database"""
    users = load_csv_data("users.csv")
    for user in users:
        if user.get('email') == email and user.get('password') == password:
            return user
    return None

def register_user(name, email, password, address):
    """Register a new customer"""
    users = load_csv_data("users.csv")
    
    # Check if email exists
    for user in users:
        if user.get('email') == email:
            return False, "Email already registered"
    
    # Add new user
    user_id = f"C-{len(users):04d}"
    users.append({
        "user_id": user_id,
        "name": name,
        "email": email,
        "password": password,
        "role": "CUSTOMER",
        "extra": address
    })
    
    return True, "Registration successful"

# Header
st.markdown("<h1 class='main-header'>🛍️ E-Commerce Management System</h1>", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("User Type")
user_type = st.sidebar.radio(
    "Select your role:",
    ["👥 Customer", "👨‍💼 Admin"],
    index=0
)

st.session_state.user_role = "ADMIN" if user_type == "👨‍💼 Admin" else "CUSTOMER"

st.sidebar.divider()

if st.session_state.user_role == "ADMIN":
    menu_option = st.sidebar.radio(
        "Admin Menu",
        ["📊 Dashboard", "📦 Products", "👥 Users", "📋 Orders"]
    )
else:
    menu_option = st.sidebar.radio(
        "Customer Menu",
        ["🏪 Browse Products", "🛒 Shopping Cart", "📜 My Orders"]
    )

st.sidebar.divider()

# Display cart count for customers
if st.session_state.user_role != "ADMIN":
    cart_count = sum(st.session_state.cart.values())
    if cart_count > 0:
        st.sidebar.info(f"🛒 Cart: {cart_count} items")

# Main content
if st.session_state.user_role == "ADMIN":
    # Admin Dashboard
    if menu_option == "📊 Dashboard":
            st.header("Admin Dashboard")
            
            col1, col2, col3, col4 = st.columns(4)
            
            products = load_csv_data("products.csv")
            users = load_csv_data("users.csv")
            orders = load_csv_data("orders.csv")
            
            with col1:
                st.metric("Total Products", len(products))
            with col2:
                st.metric("Total Users", len(users))
            with col3:
                st.metric("Total Orders", len(orders))
            with col4:
                total_revenue = sum(float(o.get('total', 0)) for o in orders if o.get('total'))
                st.metric("Total Revenue", f"${total_revenue:.2f}")
            
            st.divider()
            
            st.subheader("Recent Orders")
            if orders:
                df = pd.DataFrame(orders[:5])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No orders yet")
        
        elif menu_option == "📦 Products":
            st.header("Product Management")
            
            tab1, tab2 = st.tabs(["View Products", "Add Product"])
            
            with tab1:
                products = load_csv_data("products.csv")
                if products:
                    df = pd.DataFrame(products)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No products available")
            
            with tab2:
                st.subheader("Add New Product")
                prod_name = st.text_input("Product Name")
                prod_price = st.number_input("Price ($)", min_value=0.0, step=0.01)
                prod_category = st.selectbox("Category", ["Electronics", "Clothing", "Books", "Food", "Other"])
                prod_stock = st.number_input("Stock", min_value=0, step=1)
                
                if st.button("Add Product", use_container_width=True, type="primary"):
                    st.success("✓ Product added successfully!")
                    st.balloons()
        
        elif menu_option == "👥 Users":
            st.header("User Management")
            users = load_csv_data("users.csv")
            if users:
                df = pd.DataFrame(users)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No users registered yet")
        
        elif menu_option == "📋 Orders":
            st.header("Order Management")
            orders = load_csv_data("orders.csv")
            if orders:
                df = pd.DataFrame(orders)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No orders yet")
    
else:
    # Customer pages
    if menu_option == "🏪 Browse Products":
        st.header("Products")
        
        products = load_csv_data("products.csv")
        
        if not products:
            st.warning("No products available yet")
        else:
            # Filter options
            col1, col2 = st.columns([2, 1])
            with col1:
                search_term = st.text_input("Search products...")
            with col2:
                sort_by = st.selectbox("Sort by", ["Name", "Price: Low to High", "Price: High to Low"])
            
            # Filter products
            filtered_products = products
            if search_term:
                filtered_products = [p for p in products if search_term.lower() in str(p.get('name', '')).lower()]
            
            # Sort products
            if sort_by == "Price: Low to High":
                filtered_products.sort(key=lambda x: float(x.get('price', 0)))
            elif sort_by == "Price: High to Low":
                filtered_products.sort(key=lambda x: float(x.get('price', 0)), reverse=True)
            else:
                filtered_products.sort(key=lambda x: str(x.get('name', '')))
            
            if not filtered_products:
                st.info("No products found matching your search")
            else:
                # Display products in grid
                cols = st.columns(3)
                for idx, product in enumerate(filtered_products):
                    with cols[idx % 3]:
                        st.markdown(f"""
                        <div class="product-card">
                            <h4>{product.get('name', 'N/A')}</h4>
                            <p><strong>Category:</strong> {product.get('category', 'N/A')}</p>
                            <p><span class="price-tag">${float(product.get('price', 0)):.2f}</span></p>
                            <p><small>Stock: {product.get('stock', 0)}</small></p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        qty = st.number_input(
                            "Quantity",
                            min_value=1,
                            max_value=int(product.get('stock', 0)),
                            key=f"qty_{product.get('product_id')}"
                        )
                        
                        if st.button(
                            "🛒 Add to Cart",
                            key=f"add_{product.get('product_id')}",
                            use_container_width=True
                        ):
                            prod_id = product.get('product_id')
                            st.session_state.cart[prod_id] = qty
                            st.success(f"Added {qty} x {product.get('name')} to cart!")
    
    elif menu_option == "🛒 Shopping Cart":
        st.header("Shopping Cart")
        
        if not st.session_state.cart:
            st.info("Your cart is empty")
        else:
            products = load_csv_data("products.csv")
            products_dict = {p.get('product_id'): p for p in products}
            
            cart_items = []
            total = 0
            
            for prod_id, qty in st.session_state.cart.items():
                product = products_dict.get(prod_id)
                if product:
                    price = float(product.get('price', 0))
                    item_total = price * qty
                    total += item_total
                    cart_items.append({
                        "Product": product.get('name'),
                        "Quantity": qty,
                        "Price": f"${price:.2f}",
                        "Total": f"${item_total:.2f}"
                    })
            
            if cart_items:
                df = pd.DataFrame(cart_items)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.divider()
                st.metric("Cart Total", f"${total:.2f}")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("🧹 Clear Cart", use_container_width=True):
                        st.session_state.cart = {}
                        st.rerun()
                
                with col2:
                    if st.button("💳 Checkout", use_container_width=True, type="primary"):
                        order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                        st.session_state.orders.append({
                            "order_id": order_id,
                            "customer_email": st.session_state.user_email,
                            "total": total,
                            "items": len(cart_items),
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "status": "PENDING"
                        })
                        st.session_state.cart = {}
                        
                        st.success("✓ Order placed successfully!")
                        st.info(f"Order ID: {order_id}")
                        st.balloons()
    
    elif menu_option == "📜 My Orders":
        st.header("Order History")
        
        if not st.session_state.orders:
            st.info("You haven't placed any orders yet")
        else:
            df = pd.DataFrame(st.session_state.orders)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.divider()
            
            total_spent = sum(float(o.get('total', 0)) for o in st.session_state.orders)
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.metric("Total Orders", len(st.session_state.orders))
            with col2:
                st.metric("Total Spent", f"${total_spent:.2f}")
# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; margin-top: 2rem;'>
    <p>🏪 E-Commerce Management System v1.0.0</p>
    <p>Built with Streamlit | <a href='https://github.com/sangamsharma2152/Ecom' target='_blank'>GitHub</a></p>
</div>
""", unsafe_allow_html=True)
