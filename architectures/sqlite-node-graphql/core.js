require('dotenv').config();
const express = require('express');
const { graphqlHTTP } = require('express-graphql');

const { authenticateTokenMiddleware, makeAddUserRolesMiddleware } = require('./Auth/application');
const make_schema = require('./GraphQL/Schema');
const CoreBuilder = require('./GraphQL/CoreBuilder');
const Builder = require('./GraphQL/Builder');
const { Catalogue } = require('./GraphQL/Catalogue');
const Data = require('./DB/data');
const Loader = require('./Filters/loader');
const DataLoaderResolver = require('./Filters/DataLoaderResolver');
const AuthFilter = require('./Filters/AuthFilter');
const GraphQLFilter = require('./Filters/GraphQLFilter');
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

    const filters = new AuthFilter(
      new GraphQLFilter(
        new DataLoaderResolver(
          new Loader(data)
        )
      )
    );

    const clearCacheMiddleware = (req, res, next) => {
        filters.clearAll();
        next();
    };

    const catalogue = Builder.build(
        CoreBuilder.build(new Catalogue(), filters),
        filters
    );

    app.use('/graphql',
        clearCacheMiddleware,
        authenticateTokenMiddleware,
        makeAddUserRolesMiddleware(data),
        graphqlHTTP({
            schema: make_schema(catalogue),
            graphiql: process.env.NODE_ENV === 'development',
        })
    );

    app.listen(parseInt(values.port || '4000'));
    console.log('Running a GraphQL API server at http://localhost:4000/graphql');
})();
