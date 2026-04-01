from flask import Flask, render_template, request, session, redirect, url_for, jsonify, send_from_directory, make_response
import sqlite3
import os
def g():
    return {        'Content-Security-Policy': 'upgrade-insecure-requests; default-src https:',
        'X-XSS-Protection': '1; mode=block',
        'X-Frame-Options': 'SAMEORIGIN',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Robots-Tag': 'noindex',
        'Permissions-Policy': 'none',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Feature-Policy': 'none',
        'Cross-Origin-Resource-Policy': 'same-site'    }

def get_db_connection():
    conn = sqlite3.connect('shopeasy.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.secret_key = 'super_secret_session_key' # Insecure static key

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
    app.response.headers.extend(g())
    return render_template('index.html', products=products, query=query)

# Rest of the app remains the same, just added g() function for security headers