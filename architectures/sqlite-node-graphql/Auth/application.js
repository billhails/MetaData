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

function makeAddUserRolesMiddleware(data) {
    return async (req, res, next) => {
        if (req.user) {
            try {
                const roles = await data.getAuthRolesForOwner(req.user.sub);
                req.user.roles = roles.map(role => role.role);
            } catch(error) {
                logger.error('makeAddUserRolesMiddleware caught', error);
                res.sendStatus(500);
                return;
            }
        }
        next();
    };
}

module.exports = { authenticateTokenMiddleware, makeAddUserRolesMiddleware };