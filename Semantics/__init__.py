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
class Semantics:
    type = "*undefined*"
    name = None

    def __init__(self, attributes):
        self.attributes = attributes
        if 'name' in attributes:
            self.name = attributes['name']

    def __str__(self):
        return self.str(0)

    def required_attributes(self):
        return ['name']

    def optional_attributes(self):
        return []

    def str(self, depth):
        return self.pad(depth) + self.type + " " + str(self.attributes)

    def validate(self):
        for attribute in self.required_attributes():
            if attribute not in self.attributes:
                raise SemanticException(
                    "required attribute {attribute} for {type} not found".format(attribute=attribute, type=self.type)
                )
        for attribute in self.attributes:
            if attribute not in self.required_attributes() and attribute not in self.optional_attributes():
                raise SemanticException(
                    "unrecognised attribute {attribute} for {type}".format(attribute=attribute, type=self.type)
                )

    def validate_attribute(self, attribute, values):
        if attribute in self.attributes and not self.attributes[attribute] in values:
            raise SemanticException(
                "unrecognised value for {type} '{name}': {attr}='{val}', allowed values: {values}".format(
                    val=self.attributes[attribute],
                    type=self.type,
                    name=self.name,
                    attr=attribute,
                    values=', '.join(values)
                )
            )

    def get_name(self):
        return self.attributes['name']

    @staticmethod
    def pad(depth):
        return " " * depth * 4

    def attribute_value(self, attribute, value):
        return attribute in self.attributes and self.attributes[attribute] == value

    def is_auth_enabled(self):
        raise NotImplementedError('child class should implement is_auth_enabled')
    def is_auth_role(self, role):
        return self.is_auth_enabled() and self.attribute_value('auth-role', role)

    def debug(self, message):
        print(message)
        return ''

class SemanticException(Exception):
    pass

