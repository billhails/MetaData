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

class Semantics:
    """
    This is the base class for the semantics class hierarchy, it represents
    any abstract xml tag and collects common methods.
    """

    type = "*undefined*"

    def __init__(self, attributes):
        self.attributes = attributes
        if 'name' in attributes:
            self.name = attributes['name']
        else:
            self.name = None

    def __str__(self):
        return self.str(0)

    def required_attributes(self):
        return [{'name': 'name'}]

    def required_attribute_names(self):
        return [attribute['name'] for attribute in self.required_attributes()]

    def optional_attribute_names(self):
        return [attribute['name'] for attribute in self.optional_attributes()]

    def optional_attributes(self):
        return []

    def str(self, depth):
        return self.pad(depth) + self.type + " " + str(self.attributes)

    def validate(self):
        for required_attribute in self.required_attributes():
            if required_attribute['name'] not in self.attributes:
                raise SemanticException(
                    "required attribute {attribute} for {type} not found".format(
                        attribute=required_attribute['name'],
                        type=self.type
                    )
                )
            if 'values' in required_attribute:
                if self.attributes[required_attribute['name']] not in required_attribute['values']:
                    raise SemanticException(
                        "unrecognised value '{value}' for attribute '{attribute}', allowed values: {values}".format(
                            value=self.attributes[required_attribute['name']],
                            attribute=required_attribute['name'],
                            values=required_attribute['values']
                        )
                    )
        for attribute_name in self.attributes:
            if attribute_name not in self.required_attribute_names() and attribute_name not in self.optional_attribute_names():
                raise SemanticException(
                    "unrecognised attribute '{attribute}' for {type}".format(attribute=attribute_name, type=self.type)
                )
        for optional_attribute in self.optional_attributes():
            if optional_attribute['name'] in self.attributes:
                if 'values' in optional_attribute:
                    if self.attributes[optional_attribute['name']] not in optional_attribute['values']:
                        raise SemanticException(
                            "unrecognised value '{value}' for attribute '{attribute}', allowed values: {values}".format(
                                value=self.attributes[optional_attribute['name']],
                                attribute=optional_attribute['name'],
                                values=optional_attribute['values']
                            )
                        )
            elif 'default' in optional_attribute:
                self.attributes[optional_attribute['name']] = optional_attribute['default']

    def get_name(self):
        return self.attributes['name']

    @staticmethod
    def pad(depth):
        return " " * depth * 4

    def attribute_value(self, attribute, value):
        return self.has_attribute(attribute) and self.attributes[attribute] == value

    def has_attribute(self, attribute):
        return attribute in self.attributes

    def is_auth_enabled(self):
        raise NotImplementedError('child class should implement is_auth_enabled')

    def is_auth_role(self, role):
        return self.is_auth_enabled() and self.attribute_value('auth-role', role)

    def is_auth_visibility(self, visibility):
        return self.is_auth_enabled() and self.attribute_value('auth-visibility', visibility)

    def is_auth_access(self, access):
        return self.is_auth_enabled() and self.attribute_value('auth-access', access)

    def has_attribute_not(self, attribute, value):
        return self.has_attribute(attribute) and not self.attribute_value(attribute, value)

    def auth_visibility(self):
        return self.attributes['auth-visibility']

    def debug(self, message):
        print(message)
        return ''

    def throw(self, error):
        raise SemanticException(error)

class SemanticException(Exception):
    pass

