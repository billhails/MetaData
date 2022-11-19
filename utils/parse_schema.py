import xml.etree.ElementTree as eT
from Semantics.Association import Association
from Semantics.Description import Description
from Semantics.Entity import Entity
from Semantics.Field import Field
from Semantics.Reference import Reference
from Semantics.Schema import Schema
from Semantics.Union import Union


def parse_schema(node):
    match node.tag:
        case 'schema':
            return Schema(node.attrib, [parse_schema(n) for n in node])
        case 'entity':
            return Entity(node.attrib, [parse_schema(n) for n in node])
        case 'description':
            return Description(node.text)
        case 'field':
            return Field(node.attrib)
        case 'reference':
            return Reference(node.attrib)
        case 'union':
            return Union(node.attrib, [parse_schema(n) for n in node])
        case 'association':
            return Association(node.attrib)
        case _:
            raise "Error unrecognised node type {}".format(node.tag)


def get_semantics(schema):
    my_tree = eT.parse(schema)
    semantics = parse_schema(my_tree.getroot())
    semantics.validate()
    semantics.build()
    return semantics
