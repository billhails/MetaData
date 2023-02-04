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
from Semantics import Semantics, SemanticException

class Field(Semantics):
    """
    This class represents a <field> element within an <entity> element
    """

    entity = None
    type = "Field"

    def __init__(self, attributes, components):
        if len(components):
            raise SemanticException('field can not contain components')
        super().__init__(attributes)

    def build(self, entity):
        self.entity = entity

    def required_attributes(self):
        return super().required_attributes() + [
            {'name': 'type', 'values': ["text", "title", "guid", "small_string", "name", "email", "password", "token", "boolean"]}
        ]

    def optional_attributes(self):
        return super().optional_attributes() + [
            {'name': 'unique', 'values': ['n', 'y'], 'default': 'n'},
            {'name': 'auth-role', 'values': ['none', 'external-id', 'password', 'token', 'role'], 'default': 'none'},
            {'name': 'auth-visibility', 'values': ['visible', 'redacted', 'hidden'], 'default': 'visible'},
            {'name': 'default'}
        ]

    def get_type(self):
        return self.attributes['type']

    def is_xss_susceptible(self):
        return self.get_schema().is_xss_secure() and self.get_type() in ["text", "title", "guid", "small_string", "name", "email"]

    def get_entity(self):
        return self.entity

    def is_unique(self):
        return self.attribute_value('unique', 'y')

    def is_auth(self):
        return self.has_attribute_not('auth-role', 'none') or self.has_attribute_not('auth-visibility', 'visible')

    def get_schema(self):
        return self.get_entity().get_schema()

    def is_auth_enabled(self):
        return self.get_schema().is_auth_enabled()

    def has_default(self):
        return self.has_attribute('default')

    def get_default(self):
        return self.attributes['default']