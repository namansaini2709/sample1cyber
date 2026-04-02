// Recommended secure approach using .env file with restricted access
const dotenv = require('dotenv');

// Load .env file in the main entry point of the application
process.env.NODE_ENV === 'production' ? dotenv.config({ path: __dirname + '/.env' }) : dotenv.config({ silent: true });

// Use a secure secrets manager or a dedicated environment config service in the app
const mySecretKey = process.env.MY_SECRET_KEY;