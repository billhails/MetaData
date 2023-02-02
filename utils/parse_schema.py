#
#  MetaData - API Generator.
#  Copyright (C) 2022-2023  Bill Hails
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
from Semantics import SemanticException


def parse_schema(node):
    match node.tag:
        case 'schema':
            return Schema(node.attrib, [parse_schema(n) for n in node])
        case 'entity':
            return Entity(node.attrib, [parse_schema(n) for n in node])
        case 'description':
            return Description(node.attrib, [parse_schema(n) for n in node], node.text)
        case 'field':
            return Field(node.attrib, [parse_schema(n) for n in node])
        case 'reference':
            return Reference(node.attrib, [parse_schema(n) for n in node])
        case 'union':
            return Union(node.attrib, [parse_schema(n) for n in node])
        case 'association':
            return Association(node.attrib, [parse_schema(n) for n in node])
        case _:
            raise "Error unrecognised node type {}".format(node.tag)


def get_semantics(schema):
    tree = eT.parse(schema)
    root = tree.getroot()
    if root.get('auth') == 'enabled':
        # if auth is enabled then we stitch in an extra schema fragment that contains auth entities etc.
        owner_entity = None
        for entity in root.findall('entity'):
            if entity.get('auth-role') == 'owner':
                owner_entity = entity
                break
        if owner_entity is None:
            raise SemanticException('schema has auth=enabled but no entity with auth-role=owner was found')
        if not owner_entity.get('name'):
            raise SemanticException("auth-role=owner entity has no 'name' attribute")
        auth_tree = eT.parse('./data/auth-fragment.xml')
        auth_root = auth_tree.getroot()
        for entity in auth_root:
            if entity.tag == 'association' and entity.get('auth-role') == 'role':
                entity.attrib['lhs'] = owner_entity.get('name')
            root.append(entity)
    semantics = parse_schema(root)
    semantics.build()
    semantics.validate()
    return semantics
