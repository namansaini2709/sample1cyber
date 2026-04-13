
from flask import Flask
app = Flask(__name__)
from flask_security import current_user

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.after_request
def after_request(response):
  response.headers['Content-Security-Policy'] = "upgrade-insecure-requests; default-src 'self'; script-src 'self' https://cdn.example.com;/ style-src 'self' https://fonts.googleapis.com/