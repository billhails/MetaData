const logger = require('./logger');

const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const base64Pattern = /^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/;

function idToCursor(id) {
    if (uuidPattern.test(id)) {
        return Buffer.from(id.replaceAll('-', ''), 'hex').toString('base64');
    }
    logger.error('invalid id cannot be converted to cursor', {id});
    return null;
}

function cursorToId(cursor) {
    if (!base64Pattern.test(cursor)) {
        logger.error('invalid cursor cannot be converted to uuid (regex match failed)', {cursor});
        return null;
    }

    const hex = Buffer.from(cursor, 'base64').toString('hex');

    if (hex.length !== 32) {
        logger.error('invalid cursor cannot be converted to uuid (wrong size)', {cursor});
        return null;
    }

    const uuid = [
        hex.substring(0, 8),
        hex.substring(8, 12),
        hex.substring(12, 16),
        hex.substring(16, 20),
        hex.substring(20, 32)
    ].join('-');

    if (!uuidPattern.test(uuid)) {
        // first char of the fourth group must match [89ab]
        logger.error('invalid cursor cannot be converted to uuid (bad uuid version)', {cursor});
        return null;
    }

    return uuid;
}

module.exports = { idToCursor, cursorToId }