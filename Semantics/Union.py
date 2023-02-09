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
from Semantics.Container import Container


class Union(Container):
    """
    This class represents a <union> element (discriminated union of references)
    contained by an <entity> and containing <reference> elements
    """

    type = "Union"
    allowed_components = ['Reference']

    def __init__(self, attributes, components):
        super().__init__(attributes, components)
        self.container = None

    def is_auth_enabled(self):
        return self.container.is_auth_enabled()

    def build(self, entity):
        self.container = entity
        for component in self.components:
            component.build(entity, self)

    
    def get_references(self):
        return self.components

    def size(self):
        return len(self.components)
