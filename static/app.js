
    // Fixed pattern
    import dotenv from 'dotenv';
    const path = require('path');

    const envPath = path.resolve(__dirname, '..', '.env');
    dotenv.config({ path: envPath, silent: true });
   