const express = require('express');
const app = express();
app.get('/api/data', addSecurityHeaders, function(req, res){ ... });
function addSecurityHeaders(req, res, next) {
    res.header('Content-Security-Policy', 'default-src https:;
        script-src https: http: localhost 127.0.0.1;
        style-src https: http: font-src https: http:;
        object-src https:;
        img-src https: http: data:
        frame-src https: http:;
        worker-src https:;
        child-src https:;
        connect-src https: http:;
        media-src https:;
    ');
    res.header('X-DNS-Prefetch-Control', 'off');
    res.header('Cross-Origin-Resource-Policy', 'cross-origin');
    res.header('Cross-Origin-Opener-Policy', 'same-origin');
    res.header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
    res.header('X-Content-Type-Options', 'nosniff');
    res.header('X-XSS-Protection', '1; mode=block');
    res.header('Referrer-Policy', 'no-referrer');
    res.header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
    next();
}
