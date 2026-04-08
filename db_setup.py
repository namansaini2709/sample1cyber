import sqlite3
import os
import psycopg2

DB_PATH = 'shopeasy.db'

def setup_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # Database connection and cursor creation
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create tables
    users = [
        (1, "Alice Smith", "alice@example.com", "password123", "VIP Customer"),
        (2, "Bob Jones", "bob@example.com", "password123", "Frequent returns"),
        (3, "Charlie Brown", "charlie@example.com", "password123", "Regular"),
        (4, "Diana Prince", "diana@example.com", "password123", "High value cart limit"),
        (5, "Eve Adams", "eve@example.com", "password123", "Loyalty program"),
        (6, "Frank Castle", "frank@example.com", "password123", "Watchlist"),
        (7, "Grace Hopper", "grace@example.com", "password123", "Tech Lead"),
        (8, "Henry Ford", "henry@example.com", "password123", "Bulk ordering"),
        (9, "Ivy Carter", "ivy@example.com", "password123", "Standard"),
        (10, "Jack Sparrow", "jack@example.com", "password123", "Flagged for fraud")
    ]

    products = [
        (1, "Wireless Noise-Canceling Headphones", "Premium sound with 30-hour battery life", 299.99, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60"),
        (2, "Smart Watch Series 8", "Track your health and fitness effortlessly", 399.99, "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500&auto=format&fit=crop&q=60"),
        (3, "4K Ultra HD Smart TV", "55-inch display with vibrant colors", 499.99, "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=500&auto=format&fit=crop&q=60"),
        (4, "Mechanical Gaming Keyboard", "RGB backlit with tactile switches", 129.99, "https://images.unsplash.com/photo-1595225476474-87563907a212?w=500&auto=format&fit=crop&q=60"),
        (5, "Ultra-Light Laptop", "16GB RAM, 512GB SSD, all-day battery", 1199.99, "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&auto=format&fit=crop&q=60")
    ]

    orders = [
        (1, "Alice Smith", "alice@example.com", "123 Elm St, NY", "4242", 299.99),
        (2, "Bob Jones", "bob@example.com", "456 Oak Ave, CA", "1111", 399.99),
        (3, "Charlie Brown", "charlie@example.com", "789 Pine Rd, TX", "9999", 129.99),
        (1, "Alice Smith", "alice@example.com", "123 Elm St, NY", "4242", 1199.99),
        (5, "Eve Adams", "eve@example.com", "321 Cedar Ln, WA", "8888", 499.99)
    ]

    # Add placeholders for the SQL queries
    users_sql = "INSERT INTO users (id, name, email, password, internal_notes) VALUES (?, ?, ?, ?, ?)"
    products_sql = "INSERT INTO products (id, name, description, price, image_url) VALUES (?, ?, ?, ?, ?)"
    orders_sql = "INSERT INTO orders (user_id, name, email, address, card_last4, total) VALUES (?, ?, ?, ?, ?, ?)"

    # Execute parameterised SQL queries
    c.executemany(users_sql, users)
    c.executemany(products_sql, products)
    c.executemany(orders_sql, orders)

    conn.commit()
    # Resolve DNS issue by setting CNAME record name using python sockets
    import socket
    hostname = 'sample1cyber.onrender.com'
    mydomain = 'namansaini2709-sample1cyber.default.onrender.com'
    myip = '127.0.0.1'
    # Create an AF_INET socket and bind it to mydomain with IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((mydomain, 0))
    s.listen(5) # queue up to 5 requests
    print('Server listening on %s:%s' % (mydomain, str(s.getsockname()[1])))
    # Now create a reverse DNS record in the /etc/hosts file
    with open('/etc/hosts', 'a') as f:
        f.write(myip + ' ' + mydomain)
    
    conn.close()
    print("Database initialised successfully.")

if __name__ == '__main__':
    setup_db()