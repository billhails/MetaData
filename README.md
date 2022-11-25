# MetaData

MetaData is a code-generation system that takes a single XML file describing a data model (entities
and their relationships) and generates a complete backend application, consisting of a database
and a GraphQL interface to that database. The code generation system is written in Python, and
in the first instance the generated database is SQLite and the generated GraphQL stack is node js.

I'd wanted to rename this project "Marmite" because firstly code-generation is a very polarising
subject, people tend to either love it or hate it, and secondly the templates in particular
are very information-rich. However I'd probably run into issues using a likely proprietary name
so MetaData will have to do.

## Build the Code Generator

On Unix/Linux, clone the repo, then in the root directory do

```commandline
python --version # requires 3.x
virtualenv --python=pythonX.Y `pwd`/venv # use the python version output from the previous command
pip install -r requirements.txt
```

## Generate the Demo Application

The provided [demo/schema.xml](demo/schema.xml) shows how to declare entities and their relationships, and
the sample target application can be generated by:

```commandline
python3 main.py --schema demo/schema.xml --output demo/out --architecture sqlite-node-graphql
```

This will create the directory `demo/out` if it doesn't exist and populate it with the generated application.

Note that the argument to `--architecture` is just the name of a directory under `./architectures`
containing appropriate templates. The intention is to support more architectures in the future.

To run the generated application:

```commandline
cd demo/out
npm install     # first time - install node js dependencies
npm run init-db # first time - creates the empty database
npm run dev     # run the application on http://localhost:4000/graphql
```

If you want to import some test data, there's a file [demo/data.sql](demo/data.sql) that can
be fed to `sqlite` by running:

```commandline
sqlite3 demo.db < ../data.sql
```

from the `demo/out` directory.

## Structure of the Builder Application

### Architectures

The directory structure under individual architectures is completely free form and is replicated to
the directory specified by the `--output` argument to the builder. The templates are processed using
[jinja2](https://palletsprojects.com/p/jinja/). Files with a `.j2` suffix are considered jinja
templates and are processed to the equivalent output file with the `.j2` suffix stripped.
Normally files are processed passing in a top-level `schema` object representing the entire application
specification, however `.j2` files with a `%E` embedded in their name are instead processed
repeatedly for each `entity` in the schema, and written to separate files with the `%E` replaced by each
entity name. Files with a `.j2h` suffix are considered macros and ignored
(though they can be imported). Files without a `.j2` suffix are copied to the output verbatim.

### Semantics

The mistake often made with code generation is to parse some XML to a basic DOM then pass that directly to
the templates. That requires the templates to do an awful lot of work just to get at the data
they require. Instead this application further processes the parsed XML into a highly self-referential
graph of semantic objects which have high-level methods like `schema.get_entities()` and
`entity.get_fields()` making the maintenance of the templates much more practical.

## TODO

Lots, but specifically
* General
  * business logic
  * local template overrides
  * Think about how to share templates across architectures (later)
* sqlite-node-graphql Architecture Specific
  * tests (generated)
  * auth
  * enumeration data type
  * more data types
  * deferred data retrieval - done (but dataloader is sub-optimal)
    * separate dataloader per request - or cache management
  * pagination - basic pagination done
  * mutation - done for add
  * OpenTracing or OpenTelemetry metrics
