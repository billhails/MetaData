
const logger = require('../Utils/logger');

class Catalogue {
    types = {};
    memoizedTypes = {};
    queries = {};
    memoizedQueries = {};
    mutations = {};
    memoizedMutations = {};

    addType(name, definitionFn) {
        if (name in this.types) {
            this.error(`attempt to redefine GraphQL type "${name}"`);
        }
        this.types[name] = definitionFn;
    }

    getType(name) {
        if (!(name in this.memoizedTypes)) {
            if (name in this.types) {
                this.memoizedTypes[name] = this.types[name](this);
            } else {
                this.error(`attempt to retrieve undefined GraphQL type "${name}"`);
            }
        }
        return this.memoizedTypes[name];
    }

    addQuery(name, definitionFn) {
        if (name in this.queries) {
            this.error(`attempt to redefine GraphQL query "${name}"`);
        }
        this.queries[name] = definitionFn;
    }

    getQuery(name) {
        if (!(name in this.memoizedQueries)) {
            if (name in this.queries) {
                this.memoizedQueries[name] = this.queries[name](this);
            } else {
                this.error(`attempt to retrieve undefined GraphQL query "${name}"`);
            }
        }
        return this.memoizedQueries[name];
    }

    getAllQueries() {
        return Object.keys(this.queries).sort().reduce((acc, name) => ({...acc, [name]: this.getQuery(name)}), {});
    }

    addMutation(name, definitionFn) {
        if (name in this.mutations) {
            this.error(`attempt to redefine GraphQL mutation "${name}"`);
        }
        this.mutations[name] = definitionFn;
    }

    getMutation(name) {
        if (!(name in this.memoizedMutations)) {
            if (name in this.mutations) {
                this.memoizedMutations[name] = this.mutations[name](this);
            } else {
                this.error(`attempt to retrieve undefined GraphQL mutation "${name}"`);
            }
        }
        return this.memoizedMutations[name];
    }

    getAllMutations() {
        return Object.keys(this.mutations).sort().reduce((acc, name) => ({...acc, [name]: this.getMutation(name)}), {});
    }

    error(message) {
        logger.error(message);
        throw new Error(message);
    }
}

module.exports = { Catalogue };