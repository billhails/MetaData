# Dev Notes

Random scribblings in one place.

## Architectures

Thinking about how to organize architectures better, for example two architectures that share
the same language (node, php, ...) and api (ReST, GraphQL, SOAP(!) ...) but only differ by
backend database will have most files in common, the only things different will likely be
the `data` and `database_schema` files.

The following file structure might support this
```text
+--architectures-+-language-+-node-+-api-+-graphql-+-common---
                 |          |      |     |         |
                 |          |      |     |         +-database-+-sqlite--- # graphql-specific sqlite tweaks
                 |          |      |     |
                 |          |      |     +-rest-+-common---               # database agnostic rest php
                 |          |      |            |
                 |          |      |            +-database-+-sqlite---    # rest-specific sqlite tweaks
                 |          |      |                       |
                 |          |      |                       +-mysql---     # rest-specific mysql tweaks
                 |          |      |
                 |          |      +-database-+-sqlite---                 # generic php sqliten
                 |          |      |          |
                 |          |      |          +-mysql---                  # generic php mysql
                 |          |      |
                 |          |      +-common---                            # files common across all php
                 |          |
                 |          +-node---
                 |
                 +-common--- # totally generic files
```

This is complicated, maybe there's a different approach using a 3D matrix:
(language × platform × database),
where each dimension has a generic component: (generic, php, node)?

So how to represent a 3d matrix as a directory tree (or should we)?

Let's try 2 × 2 × 2.

(A, B) × (1, 2) × (x, y) is 8 locations:
* (A, 1, x)
* (A, 1, y)
* (A, 2, x)
* (A, 2, y)
* (B, 1, x)
* (B, 1, y)
* (B, 2, x)
* (B, 2, y)

which is just
```text
+-A-+-1-+-x
|   |   |
|   |   +-y
|   |
|   +-2-+-x
```

etc.
Of course A, 1, and x are generic, so B, 2 and y need their own subdirectories to avoid
possible name conflicts:
```text
+-generic-+-generic-+-generic
|         |         |
|         |         +-specific-+-y
|         |                    |
|         |                    +-z
|         |
|         +-specific-+-2-+-generic
|                    |   |
|                    |   +-specific-+-y
|                    |              |
|                    |              +-z
|                    |
|                    +-3-+-generic
|                        |
|                        +-specific-+-y
|                                   |
|                                   +-z
|
+-specific-+-B----
```
etc.

That definitely works, but is it usable?

```text
+-generic-+-generic-+-generic
|         |         |
|         |         +-specific-+-sqlite
|         |                    |
|         |                    +-mysql
|         |
|         +-specific-+-graphql-+-generic
|                    |         |
|                    |         +-specific-+-sqlite
|                    |                    |
|                    |                    +-mysql
|                    |
|                    +-rest-+-generic
|                           |
|                           +-specific-+-sqlite
|                                      |
|                                      +-mysql
|
+-specific-+-node----
           |
           +-php---
```

We could simply maintain by convention that the order is language, platform, database; or we
could add extra depth `language/generic`, `language/specific`,
`language/specific/php/platform/generic/database/specific/sqlite` etc.

With this structure we only ever populate the leaf nodes with templates.

Of course this still leaves problems. If a template is found in a completely specific
location then obviously for that specific architecture it overrides any other such template.
But what if the template exists at two partially generic locations, say
`generic/graphql/generic` and `node/generic/generic`? We would need to impose a search order
that is at least deterministic, and it should favour more specific locations.

Simple binary ordering?

* S/S/S
* S/S/G
* S/G/S
* S/G/G
* G/S/S
* G/S/G
* G/G/S
* G/G/G

Not really. G/S/S sorts after S/G/G even though G/S/S has two specific components
while S/G/G has only one. So maybe order by number of specific components then binary
order?

* 3
  * S/S/S
* 2
  * S/S/G
  * S/G/S
  * G/S/S
* 1
  * S/G/G
  * G/S/G
  * G/G/S
* 0
  * G/G/G

Looks like there is no generic solution that will satisfy all requirements,
this may be as close as we can get.