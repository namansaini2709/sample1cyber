const authenticate = (req, res, next) => {
    if (req.isAuthenticated()) {
        return next();
    }
    res.status(401).send({ error: 'Unauthorized' });
};

app.get('/api/v1/sample', authenticate, (req, res) => {
    if (req.user) {
        res.json({ message: 'Hello' });
    } else {
        res.status(403).send({ error: 'Forbidden' });
    }
});