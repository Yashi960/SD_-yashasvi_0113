import streamlit as st
import pymysql  # <-- Swapped this from mysql.connector!
import pandas as pd

# Set up page configuration to match your exact dashboard theme
st.set_page_config(page_title="Fake Review Detection System", page_icon="⭐", layout="wide")

# --- DATABASE CONNECTION FUNCTION ---
def get_mysql_connection():
    """Connects straight to your live MySQL Workbench server schema via PyMySQL"""
    return pymysql.connect(
        host="localhost",
        user="root",
        password="sn060805",  
        database="fake_review_db",
        cursorclass=pymysql.cursors.Cursor  # Handles data mapping cleanly
    )

def check_review_rules(review_text, selected_product):
    review = review_text.lower().strip()

    # Rule 1: Very short review
    if len(review) < 8:
        return "Fake"

    # Rule 2: Spam URLs
    spam_keywords = [
        "www.", "http", "https", ".com", ".net", ".org",
        "click here", "visit now", "check this", "bit.ly",
        "tinyurl", "link", "telegram", "whatsapp"
    ]
    if any(word in review for word in spam_keywords):
        return "Fake"



    # Rule 3: Promotional / Fake marketing words
    fake_keywords = [
        "buy now", "limited offer", "best offer", "100% genuine",
        "guaranteed", "free gift", "exclusive deal", "hurry up",
        "discount", "sale", "cashback", "coupon", "promo code",
        "don't miss", "order now", "worth every penny",
        "life changing", "absolute perfection", "must buy",
        "highly highly recommend", "best ever", "amazing amazing",
        "superb product", "excellent product", "five stars",
        "10/10", "perfect product", "unbelievable", "miracle",
        "awesome", "fantastic", "mind blowing"
    ]
    if any(word in review for word in fake_keywords):
        return "Fake"

    # Rule 4: Too many repeated characters
    repeated = [
        "!!!!!", "?????", ".....", "hahaha", "lolllll",
        "sooooo", "gooooood", "niiiice", "woooooow"
    ]
    if any(word in review for word in repeated):
        return "Fake"

    # Rule 5: Too many emojis
    emoji_count = sum(review.count(e) for e in ["😀","😂","😍","🔥","❤️","👍","👏","🎉","💯","😊"])
    if emoji_count >= 4:
        return "Fake"

    # Rule 6: Same word repeated many times
    words = review.split()
    if len(words) > 6:
        for word in set(words):
            if words.count(word) >= 5:
                return "Fake"

    # Rule 7: ALL CAPS
    if review_text.isupper() and len(review_text) > 10:
        return "Fake"

    # Rule 8: Product mismatch
    product = selected_product.lower()

    if "hotel" in product or "resort" in product or "spa" in product:
        mismatch = [
            "battery", "charger", "mobile", "phone",
            "laptop", "shoe", "shirt", "delivery",
            "camera", "headphone"
        ]
        if any(word in review for word in mismatch):
            return "Fake"

    # Rule 9: Suspicious usernames
    suspicious = [
        "seller", "owner", "official", "admin",
        "support team", "company"
    ]
    if any(word in review for word in suspicious):
        return "Fake"

    # Rule 10: Excessive punctuation
    punctuation = review.count("!") + review.count("?")
    if punctuation >= 8:
        return "Fake"

    return "Authentic"


# --- SIDEBAR NAVIGATION MENU (EXACT MATCH TO YOUR SLIDES) ---
st.sidebar.title("📋 Menu")
menu_selection = st.sidebar.radio(
    "Go to page:",
    ["Dashboard", "Add User", "Add Product", "Add Review", "View Reviews", "Fake Reviews"]
)


# --- PAGE 1: DASHBOARD ---
if menu_selection == "Dashboard":
    st.title("⭐ Fake Review Detection System")
    
    # Fetch live counts dynamically from MySQL tables
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM reviews")
        total_reviews = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM reviews WHERE status='Fake'")
        fake_reviews = cursor.fetchone()[0]
        
        conn.close()
    except Exception as e:
        st.error(f"Could not connect to MySQL server. Ensure MySQL is running. Error: {e}")
        total_users, total_products, total_reviews, fake_reviews = 0, 0, 0, 0

    # Display clean visual blocks to match your project screenshot layout
    col1, col2 = st.columns(2)
    with col1:
        st.metric("👤 Total Users", total_users)
        st.metric("📝 Total Reviews", total_reviews)
    with col2:
        st.metric("📦 Total Products", total_products)
        st.metric("🚩 Fake Reviews", fake_reviews)
    
    st.markdown("---")
    st.subheader("Project Description")
    st.write("This application detects fake reviews using a rule-based algorithm.")
    
    st.subheader("Features")
    st.markdown("- Add User\n- Add Product\n- Add Review")


# --- PAGE 2: ADD USER ---
elif menu_selection == "Add User":
    st.title("👤 Add User Profile")
    with st.form("user_form", clear_on_submit=True):
        username = st.text_input("Username")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Add User")
        
        if submit:
            if username and email and password:
                try:
                    conn = get_mysql_connection()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
                    conn.commit()
                    st.success(f"User '{username}' added successfully to MySQL!")
                    conn.close()
                except Exception as e:
                    st.error(f"Error saving to MySQL database: {e}")
            else:
                st.warning("Please complete all input boxes.")


# --- PAGE 3: ADD PRODUCT ---
elif menu_selection == "Add Product":
    st.title("📦 Product Inventory Management")
    with st.form("product_form", clear_on_submit=True):
        product_name = st.text_input("Product/Hotel Label Name")
        category = st.selectbox("Category Group", ["Electronics", "Clothing", "Hotel/Resort", "Home & Kitchen", "Other"])
        submit = st.form_submit_button("Register Product")
        
        if submit:
            if product_name:
                try:
                    conn = get_mysql_connection()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO products (product_name, category) VALUES (%s, %s)", (product_name, category))
                    conn.commit()
                    st.success(f"Registered '{product_name}' successfully!")
                    conn.close()
                except Exception as e:
                    st.error(f"Error connecting to MySQL: {e}")
            else:
                st.warning("Please type a product or hotel name.")


# --- PAGE 4: ADD REVIEW (WITH EXACT SLIDE ALGORITHM RULE) ---
elif menu_selection == "Add Review":
    st.title("✍️ Add Content Review")
    
    try:
        conn = get_mysql_connection()
        users_df = pd.read_sql_query("SELECT user_id, username FROM users", conn)
        products_df = pd.read_sql_query("SELECT product_id, product_name FROM products", conn)
        conn.close()
    except Exception as e:
        st.error(f"Database error: {e}")
        users_df, products_df = pd.DataFrame(), pd.DataFrame()
    
    if users_df.empty or products_df.empty:
        st.info("⚠️ Ensure you have at least one active User and Product available in your MySQL database lists.")
    else:
        user_map = {row['username']: row['user_id'] for _, row in users_df.iterrows()}
        product_map = {row['product_name']: row['product_id'] for _, row in products_df.iterrows()}
        
        selected_user = st.selectbox("User Selection:", list(user_map.keys()))
        selected_product = st.selectbox("Product Target Selection:", list(product_map.keys()))
        rating = st.slider("Rating Selection (1 to 5 Stars)", 1, 5, 5)
        review_text = st.text_area("Type or paste evaluation text context:")
        
        if st.button("Analyze & Save Entry"):
            if review_text.strip() == "":
                st.warning("Please provide valid context evaluation feedback.")
            else:
                # Run the exact slide algorithm function
                status_label = check_review_rules(review_text,selected_product)
                
                try:
                    conn = get_mysql_connection()
                    cursor = conn.cursor()
                    query = "INSERT INTO reviews (user_id, product_id, review_text, rating, status) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(query, (user_map[selected_user], product_map[selected_product], review_text, rating, status_label))
                    conn.commit()
                    conn.close()
                    
                    if status_label == "Fake":
                        st.error("🚨 Deceptive / Fake Review Detected according to slide criteria rules!")
                    else:
                        st.success("✅ Authentic / Real Review verified successfully.")
                except Exception as e:
                    st.error(f"MySQL write operation aborted: {e}")


# --- PAGE 5: VIEW REVIEWS ---
elif menu_selection == "View Reviews":
    st.title("📋 Full Review History Logs")
    try:
        conn = get_mysql_connection()
        query = """
            SELECT 
                r.review_id AS 'Review ID', u.username AS 'User', p.product_name AS 'Product',
                r.review_text AS 'Review Text', r.rating AS 'Rating', r.status AS 'Status'
            FROM reviews r
            LEFT JOIN users u ON r.user_id = u.user_id
            LEFT JOIN products p ON r.product_id = p.product_id
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            st.info("No logs present inside the MySQL system registry.")
        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error accessing records database layer: {e}")


# --- PAGE 6: FAKE REVIEWS FILTER ---
elif menu_selection == "Fake Reviews":
    st.title("🚩 High-Risk Spammed / Fake Content Queue")
    try:
        conn = get_mysql_connection()
        query = """
            SELECT 
                r.review_id AS 'Review ID', u.username AS 'User', p.product_name AS 'Product',
                r.review_text AS 'Flagged Content Text', r.rating AS 'Rating'
            FROM reviews r
            LEFT JOIN users u ON r.user_id = u.user_id
            LEFT JOIN products p ON r.product_id = p.product_id
            WHERE r.status = 'Fake'
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            st.success("Excellent! Zero malicious entries flagged inside the active filter database pipeline queues.")
        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Connection mapping error: {e}")