app.get('/api/data', function(req, res) {
    res.header('Content-Security-Policy', 'default-src 'self'');
    res.header('X-Content-Type-Options', 'nosniff');
    res.header('X-XSS-Protection', '1; mode=block');
    res.header('X-Frame-Options', 'SAMEORIGIN');
    // Logic to fetch and return data
    res.send(data);
  });