const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');

const make_schema = require('./GraphQL/Schema');
const Data = require('./Utils/data');
const SimpleResolver = require('./Utils/SimpleResolver');
const loader = require('./Utils/loader');
const DataLoaderResolver = require('./Utils/DataLoaderResolver');

const app = express();

const useDataLoader = true;

(async () => {
    app.use('/graphql', graphqlHTTP({
      schema: make_schema(useDataLoader ? new DataLoaderResolver(loader(await Data.build())) : new SimpleResolver(await Data.build())),
      graphiql: true,
    }));
    app.listen(4000);
    console.log('Running a GraphQL API server at http://localhost:4000/graphql');
})();
