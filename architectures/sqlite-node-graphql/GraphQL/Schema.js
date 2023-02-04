
const { GraphQLObjectType, GraphQLSchema, printSchema } = require('graphql');
const logger = require('../Utils/logger');

// Turns the catalogue into a GraphQL schema

const make_schema = (catalogue) => {

    const queryType = new GraphQLObjectType({
        name: 'Query',
        fields: () => catalogue.getAllQueries()
    });

    const mutationType = new GraphQLObjectType({
        name: 'Mutation',
        fields: () => catalogue.getAllMutations()
    });

    const schema = new GraphQLSchema({
        query: queryType,
        mutation: mutationType
    });
    // logger.debug(printSchema(schema));
    return schema;

};

module.exports = make_schema;