-- 1. Create the Schema / Database
CREATE DATABASE IF NOT EXISTS fake_review_db;
USE fake_review_db;

-- 2. Create the Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

-- 3. Create the Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- 4. Create the Reviews Table with Referential Integrity Constraints
CREATE TABLE IF NOT EXISTS reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    review_text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    status VARCHAR(20) NOT NULL,
    CONSTRAINT fk_review_user FOREIGN KEY (user_id) 
        REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_review_product FOREIGN KEY (product_id) 
        REFERENCES products(product_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 5. Insert Sample Authentic Profiles for Mock Setup
INSERT INTO users (username, email, password) VALUES 
('developer_admin', 'admin@integrity.com', 'securepass123'),
('guest_reviewer', 'guest@traveler.com', 'userpass456');

INSERT INTO products (product_name, category) VALUES 
('Grand Luxury Resort & Spa', 'Hotel/Resort'),
('Premium Wireless Headphones X', 'Electronics');