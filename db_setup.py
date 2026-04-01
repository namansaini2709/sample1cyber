import sqlite3
import os
import random
import string

DB_PATH = 'shopeasy.db'

def setup_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create tables
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            internal_notes TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image_url TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            card_last4 TEXT NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Populate Users (10 users)
    user_names = ['Alice Smith', 'Bob Jones', 'Charlie Brown', 'Diana Prince', 'Eve Adams', 'Frank Castle', 'Grace Hopper', 'Henry Ford', 'Ivy Carter', 'Jack Sparrow']
    user_emails = ['alice@example.com', 'bob@example.com', 'charlie@example.com', 'diana@example.com', 'eve@example.com', 'frank@example.com', 'grace@example.com', 'henry@example.com', 'ivy@example.com', 'jack@example.com']; user_passwords = ['password123'] * 10; user_internal_notes = ['VIP Customer', 'Frequent returns', 'Regular', 'High value cart limit', 'Loyalty program', 'Watchlist', 'Tech Lead', 'Bulk ordering', 'Standard', 'Flagged for fraud']
    for i in range(len(user_names)):
        c.execute('INSERT INTO users (name, email, password, internal_notes) VALUES (?, ?, ?, ?)', (user_names[i], user_emails[i], user_passwords[i], user_internal_notes[i]))

    # Populate Products (5 products)
    product_names = ['Wireless Noise-Canceling Headphones', 'Smart Watch Series 8', '4K Ultra HD Smart TV', 'Mechanical Gaming Keyboard', 'Ultra-Light Laptop']; product_descriptions = ['Premium sound with 30-hour battery life', 'Track your health and fitness effortlessly', '55-inch display with vibrant colors', 'RGB backlit with tactile switches', '16GB RAM, 512GB SSD, all-day battery']; product_prices = [299.99, 399.99, 499.99, 129.99, 1199.99]; product_image_urls = ['https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60', 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500&auto=format&fit=crop&q=60', 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=500&auto=format&fit=crop&q=60', 'https://images.unsplash.com/photo-1595225476474-87563907a212?w=500&auto=format&fit=crop&q=60', 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&auto=format&fit=crop&q=60']
    for i in range(len(product_names)):
        c.execute('INSERT INTO products (name, description, price, image_url) VALUES (?, ?, ?, ?)', (product_names[i], product_descriptions[i], product_prices[i], product_image_urls[i]))

    # Populate Orders
    order_user_ids = [1, 2, 3, 1, 5]; order_names = ['Alice Smith', 'Bob Jones', 'Charlie Brown', 'Alice Smith', 'Eve Adams']; order_emails = ['alice@example.com', 'bob@example.com', 'charlie@example.com', 'alice@example.com', 'eve@example.com']; order_addresses = ['123 Elm St, NY', '456 Oak Ave, CA', '789 Pine Rd, TX', '123 Elm St, NY', '321 Cedar Ln, WA']; order_card_last4 = ['4242', '1111', '9999', '4242', '8888']; order_totals = [299.99, 399.99, 129.99, 1199.99, 499.99]
    for i in range(len(order_user_ids)):
        c.execute('INSERT INTO orders (user_id, name, email, address, card_last4, total) VALUES (?, ?, ?, ?, ?, ?)', (order_user_ids[i], order_names[i], order_emails[i], order_addresses[i], order_card_last4[i], order_totals[i]))

    conn.commit()
    conn.close()
    print('Database initialised successfully.')

if __name__ == '__main__':
    setup_db()