require('dotenv').config()
const { GraphQLClient, gql } = require('graphql-request');

function getGraphQLClient(token) {
    return new GraphQLClient(
        `http://localhost:${process.env.API_PORT}/graphql`,
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