#
#  MetaData - API Generator.
#  Copyright (C) 2022  Bill Hails
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
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
