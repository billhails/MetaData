const { GraphQLClient, gql } = require('graphql-request');

function getGraphQLClient(token) {
    return new GraphQLClient(
        'http://localhost:4000/graphql',
        token ? {
            headers: {
                authorization: `Bearer ${token}`
            }
        } : {}
    );
}

module.exports = {
    getGraphQLClient,
    GraphQLClient,
    gql
};