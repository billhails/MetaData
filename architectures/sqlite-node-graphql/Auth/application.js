const jwt = require('jsonwebtoken');
const logger = require('../Utils/logger');

function authenticateTokenMiddleware(req, res, next) {
    const header = req.headers['authorization'];
    if (header) {
        const [scheme, ...parameters] = header.split(' ');
        if (scheme.toLowerCase() === 'bearer') {
            const token = parameters[0];
            jwt.verify(token, process.env.ACCESS_TOKEN_SECRET, (err, user) => {
                if (err) {
                    return res.sendStatus(403);
                }
                req.user = user;
                next();
            });
        } else {
            return res.sendStatus(401);
        }
    } else {
        next(); // allow logged-out users
    }
}

module.exports = authenticateTokenMiddleware;