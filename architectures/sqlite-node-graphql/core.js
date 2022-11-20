const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');

// Construct a schema, using GraphQL schema language
const make_schema = require('./GraphQL/Schema');
const Data = require('./data');

const app = express();

(async () => {
    app.use('/graphql', graphqlHTTP({
      schema: make_schema(await Data.build()),
      graphiql: true,
    }));
    app.listen(4000);
    console.log('Running a GraphQL API server at http://localhost:4000/graphql');
})();
