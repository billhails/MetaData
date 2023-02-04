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
from Semantics import SemanticException
from Semantics.Container import Container
from Semantics.Option import Option

class Enum(Container):
    type = "Enum"
    allowed_components = ['Option']

    def __init__(self, attributes, components):
        super().__init__(attributes, components)
        self.owner = None
        self.reference = None
        self.options = None

    def build(self, owner):
        self.owner = owner
        if owner.type == 'Entity':
            self.build_as_ref()
        elif owner.type == 'Schema':
            self.build_as_declaration()
        else:
            raise SemanticException('enum must be contained by schema or by entity')

    def build_as_ref(self):
        if len(self.components) > 0:
            raise SemanticException(f'reference enum "{self.get_name()}" cannot declare options')
        self.reference = self.owner.get_schema().find_enum(self.get_name())

    def build_as_declaration(self):
        if len(self.components) == 0:
            raise SemanticException(f'defining enum "{self.get_name()}" must declare options')
        self.options = {x.attributes['name']: x for x in self.components if isinstance(x, Option)}
        for option in self.options:
            self.options[option].build(self)

    def get_options(self):
        if self.reference is None:
            return self.options.values()
        return self.reference.get_options()

    def get_first_option(self):
        return list(self.get_options())[0]