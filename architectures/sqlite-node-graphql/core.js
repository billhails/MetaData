require('dotenv').config();
const express = require('express');
const { graphqlHTTP } = require('express-graphql');

const { authenticateTokenMiddleware, makeAddUserRolesMiddleware } = require('./Auth/application');
const make_schema = require('./GraphQL/Schema');
const CoreBuilder = require('./GraphQL/CoreBuilder');
const Builder = require('./GraphQL/Builder');
const { Catalogue } = require('./GraphQL/Catalogue');
const complexity = require('./GraphQL/Complexity');
const Data = require('./DB/data');
const Loader = require('./Filters/loader');
const DataLoaderResolver = require('./Filters/DataLoaderResolver');
const SecurityFilter = require('./Filters/SecurityFilter');
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

(async () => {
    const data = await Data.build();

    const filters = new SecurityFilter(
      new AuthFilter(
        new GraphQLFilter(
          new DataLoaderResolver(
            new Loader(data)
          )
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
        graphqlHTTP(async (request, response, { variables }) => ({
            schema: make_schema(catalogue),
            validationRules: [
                complexity(variables, 1000)
            ],
            graphiql: process.env.NODE_ENV === 'development',
        }))
    );

    const port = parseInt(values.port || '4000');
    app.listen(port);
    console.log(`Running a GraphQL API server at http://localhost:${port}/graphql`);
})();
