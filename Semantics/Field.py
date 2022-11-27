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


class Field(Semantics):
    entity = None
    type = "Field"
    required_attributes = ['name', 'type']
    known_types = [
        "string",
        "guid",
        "small_string"
    ]

    def build(self, entity):
        self.entity = entity

    def get_type(self):
        return self.attributes['type']

    def get_entity(self):
        return self.entity

    def validate(self):
        super().validate()
        if self.get_type() not in self.known_types:
            raise SemanticException(
                "unrecognised type {type} for field {entity}.{name}".format(
                    type=self.get_type(),
                    entity=self.get_entity().get_name(),
                    name=self.get_name()
                )
            )
