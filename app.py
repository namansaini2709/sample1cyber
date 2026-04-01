// After (fixed)
from flask import Flask, make_response
app = Flask(__name__)

def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; object-src 'none';"
    response.headers['X-Frame-Options'] = "DENY"
    response.headers['X-XSS-Protection'] = "1; mode=block"
    response.headers['Strict-Transport-Security'] = "max-age=31536000; includeSubDomains"
    return response

@app.after_request
def after_request(response):
    return add_security_headers(response)
