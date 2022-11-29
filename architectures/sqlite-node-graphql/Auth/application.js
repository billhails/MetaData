const jwt = require('jsonwebtoken');
const logger = require('../Utils/logger');

function authenticateTokenMiddleware(req, res, next) {
    logger.debug('authenticateTokenMiddleware');
    const header = req.headers['authorization'];
    if (header) {
        logger.debug('authenticateTokenMiddleware', {header});
        const [scheme, ...parameters] = header.split(' ');
        logger.debug('authenticateTokenMiddleware', {scheme, parameters})
        if (scheme.toLowerCase() === 'bearer') {
            const token = parameters[0];
            logger.debug('authenticateTokenMiddleware', {token});
            jwt.verify(token, process.env.ACCESS_TOKEN_SECRET, (err, user) => {
                if (err) {
                    logger.debug('authenticateTokenMiddleware', {err});
                    return res.sendStatus(403);
                }
                logger.debug('authenticateTokenMiddleware logged-in access granted', {user});
                req.user = user;
                next();
            });
        } else {
            logger.debug('authenticateTokenMiddleware unacceptable scheme');
            return res.sendStatus(401);
        }
    } else {
        logger.debug('authenticateTokenMiddleware logged-out access granted');
        next(); // allow logged-out users
    }
}

module.exports = authenticateTokenMiddleware;