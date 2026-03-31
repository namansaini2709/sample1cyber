from flask import Flask, render_template, request, session, redirect, url_for, jsonify, send_from_directory, make_response
import sqlite3
import os
import time
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_session_key' # Insecure static key

DB_PATH = 'shopeasy.db'

# Auto-setup DB if it doesn't exist (Crucial for Render ephemeral deployments)
if not os.path.exists(DB_PATH):
    from db_setup import setup_db
    setup_db()

ip_rate_limit = {}

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Rate limiting decorator
def ratelimit(max_calls, period):
    def decorator(f):
        @wraps(f)
        def rate_limited(*args, **kwargs):
            ip, method, identifier = get_identifier()

            if f in ip_rate_limit and ip == ip_rate_limit[f]['ip'] and time.time() - ip_rate_limit[f]['timestamp'] < period:
                return 'Too many requests, please try again later.', 429
            else:
                # Reset rate limit counter if period is over
                if f in ip_rate_limit and time.time() - ip_rate_limit[f]['timestamp'] >= period:
                    del ip_rate_limit[f]

                ip_rate_limit[f] = {'ip': ip, 'timestamp': time.time(), 'identifier': identifier}

            return f(*args, **kwargs)
        return rate_limited
    return decorator


@app.route('/login', methods=['GET', 'POST'])
def login():
    # ... existing login code ...
    # Return rate limited response after repeated failed attempts
    if 'error' in locals() and (locals()['error'] in ip_rate_limit and time.time() - ip_rate_limit[locals()['error']]['timestamp'] < 60):
        return 'Too many login attempts, please try again later.', 429
    else:
        # Reset rate limit counter if period is over
        if 'error' in locals() and time.time() - ip_rate_limit[locals()['error']]['timestamp'] >= 60:
            del ip_rate_limit[locals()['error']] 

        return render_template('login.html', error="Invalid credentials")

# Helper function to calculate IP, method, and identifier
def get_identifier():
    ip = request.remote_addr
    method = request.method
    identifier = request.form.get('email')
    return ip, method, identifier

# Rate limit the login endpoint to 3 attempts per minute
@app.route('/login', methods=['GET', 'POST'])
def login():
    return ratelimit(max_calls=3, period=60)(login)

# ... existing route code ...