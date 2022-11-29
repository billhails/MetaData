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
from Semantics import Semantics

class Field(Semantics):
    entity = None
    type = "Field"
    known_types = [
        "string",
        "guid",
        "small_string"
    ]

    def build(self, entity):
        self.entity = entity

    def required_attributes(self):
        return super().required_attributes() + ['type']

    def optional_attributes(self):
        return super().optional_attributes() + ['unique', 'auth-role', 'auth-redacted']

    def get_type(self):
        return self.attributes['type']

    def get_entity(self):
        return self.entity

    def validate(self):
        super().validate()
        self.validate_attribute('type', self.known_types)
        self.validate_attribute('unique', ['y', 'n'])
        self.validate_attribute('auth-role', ['external-id', 'password'])
        self.validate_attribute('auth-redacted', ['y', 'n'])

    def is_unique(self):
        return self.attribute_value('unique', 'y')

    def is_redacted(self):
        return self.is_auth_enabled() and self.attribute_value('auth-redacted', 'y')

    def get_schema(self):
        return self.get_entity().get_schema()

    def is_auth_enabled(self):
        return self.get_schema().is_auth_enabled()