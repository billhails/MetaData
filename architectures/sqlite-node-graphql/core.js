require('dotenv').config();
const express = require('express');
const { graphqlHTTP } = require('express-graphql');

const validateTokenMiddleware = require('./Auth/application');
const make_schema = require('./GraphQL/Schema');
const Data = require('./Utils/data');
const SimpleResolver = require('./Utils/SimpleResolver');
const loader = require('./Utils/loader');
const DataLoaderResolver = require('./Utils/DataLoaderResolver');
const AuthFilter = require('./Utils/AuthFilter');
const GraphQLFilter = require('./Utils/GraphQLFilter');
const { parseArgs } = require('node:util');

const cliOptions = {
    port: {
        type: 'string',
        short: 'p',
    }
};

const { values } = parseArgs({ options: cliOptions });

const app = express();

const useDataLoader = true;

(async () => {
    const data = await Data.build();
    app.use('/graphql', validateTokenMiddleware, graphqlHTTP({
      schema: make_schema(
        new AuthFilter(
          new GraphQLFilter(
            new DataLoaderResolver(
              loader(data)
            )
          )
        )
      ),
      graphiql: process.env.NODE_ENV === 'development',
    }));
    app.listen(parseInt(values.port || '4000'));
    console.log('Running a GraphQL API server at http://localhost:4000/graphql');
})();
