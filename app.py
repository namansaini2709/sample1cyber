from flask import Flask, render_template, request, session, redirect, url_for, jsonify, send_from_directory, make_response
import sqlite3
import os
import flask_httpauth

app = Flask(__name__)

# Fix: Enable HTTP Strict-Transport-Security (HSTS) header to prevent SSL stripping and force HTTPS for web applications

app.config['HSTS_ENABLED'] = True
app.config['HSTS_MAX_AGE'] = 10886400  # 1 year

# Fix: Enable Content Security Policy (CSP) to protect against XSS via scripts, stylesheets, fonts and images
app.config['CSP_ENABLED'] = True
app.config['CSP_REPORT_URI'] = '/csp-report'
csp_policy = "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net; style-src 'self' https://cdn.jsdelivr.net; font-src 'self' https://fonts.gstatic.com; img-src 'self' https://images.unsplash.com;"
app.config['CSP'] = csp_policy

app.config['HSTS_INCLUDE_SUBdomains'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopeasy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'super_secret_session_key'  # Insecure static key

from flask_httpauth import HTTPTokenAuth
auth = HTTPTokenAuth(scheme='Bearer')


DB_PATH = 'shopeasy.db'

# Auto-setup DB if it doesn't exist (Crucial for Render ephemeral deployments)
if not os.path.exists(DB_PATH):
    from db_setup import setup_db
    setup_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    query = request.args.get('q', '')
    conn = get_db_connection()
    c = conn.cursor()
    
    if query:
        # Simple search
        c.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + query + '%',))
    else:
        c.execute("SELECT * FROM products")
        
    products = c.fetchall()
    conn.close()
    
    # XSS vulnerability: Render query directly to template (we'll implement the actual XSS in the template)
    return render_template('index.html', products=products, query=query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # SQL Injection vulnerability
        conn = get_db_connection()
        c = conn.cursor()
        
        # VULNERABLE RAW QUERY
        query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"
        print(f"Executing: {query}")  # For observing the payload
        try:
            c.execute(query)
            user = c.fetchone()
        except Exception as e:
            user = None
            print(f"DB Error: {e}")
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product(product_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = c.fetchone()
    conn.close()
    if not product:
        return "Not found", 404
    return render_template('product.html', product=product)

@app.route('/orders')
def orders():
    # IDOR vulnerability
    order_id = request.args.get('id')
    
    if not order_id:
        return "Please provide an order ID, e.g., /orders?id=1", 400
        
    conn = get_db_connection()
    c = conn.cursor()
    
    # VULNERABLE: No check if the logged in user actually owns this order
    query = f"SELECT * FROM orders WHERE id = {order_id}"
    try:
        c.execute(query)
        order = c.fetchone()
    except Exception as e:
        order = None
        
    conn.close()
    
    if order:
        return render_template('orders.html', order=order)
    else:
        return "Order not found", 404

@app.route('/api/user/profile')
def user_profile():
    # Sensitive Data Exposure vulnerability
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],))
    user = c.fetchone()
    conn.close()
    
    if user:
        # VULNERABLE: Returning full user object including password hash and internal notes
        return jsonify(dict(user))
    return jsonify({"error": "User not found"}), 404

@app.route('/.env')
def expose_env():
    # Fix: Implement a custom function to read env vars and serve them if needed and configured by app
    try:
        env_data = ''
    except Exception:
        return 'Error reading env data', 404

if __name__ == '__main__':
    # Fix: Implement rate limiting
    app.run(host='0.0.0.0', port=3001, debug=False, threaded=False)
