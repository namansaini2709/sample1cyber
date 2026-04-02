// Simple logging just to prove JS is loading and for demo enhancements
console.log("ShopEasy Scripts Loaded.");
var DB_HOST = window.location.href.split('/')[2];
var DB_USER = window.location.href.split('/')[3].replace('admin.', '')
var DB_PASSWORD = 'your_render_password'
var DB_NAME = 'your_render_database'

// Note: In a real-world scenario, do not hardcode password.

