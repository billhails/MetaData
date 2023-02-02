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
from Semantics import Semantics, SemanticException


class Reference(Semantics):
    entity_from = None
    entity_to = None
    union = None
    type = "Reference"

    def __init__(self, attributes, components):
        if len(components):
            raise SemanticException('reference can not contain components')
        super().__init__(attributes)

    def build(self, entity, union=None):
        self.entity_from = entity
        self.union = union
        self.entity_to = entity.get_schema().find_entity(self.attributes['references'])
        self.entity_to.accept_referrer(self)

    def required_attributes(self):
        return super().required_attributes() + [{'name': 'references'}]

    def optional_attributes(self):
        return super().optional_attributes() + [
            {'name': 'inverse'},
            {'name': 'auth-role', 'values': ['owner', 'none'], 'default': 'none'}
        ]

    def get_referrer_name(self):
        if 'inverse' in self.attributes:
            return self.attributes['inverse']
        return self.entity_from.get_name()

    def get_entity(self):
        return self.entity_from

    def get_referenced(self):
        return self.entity_to

    def is_union(self):
        return self.union is not None

    def get_union(self):
        return self.union

    def get_column_name(self):
        if self.is_union():
            return self.union.get_name()
        return self.get_name()

    def get_schema(self):
        return self.get_entity().get_schema()

    def is_auth_enabled(self):
        return self.get_schema().is_auth_enabled()
