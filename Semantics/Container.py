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


class Container(Semantics):
    allowed_components = []

    def __init__(self, attributes, components):
        super().__init__(attributes)
        self.components = components

    def str(self, depth):
        prefix = super().str(depth)
        return "{prefix} {{\n{body}\n{pad}}}".format(prefix=super().str(depth),
                                                     body="\n".join([x.str(depth+1) for x in self.components]),
                                                     pad=self.pad(depth))

    def validate(self):
        super().validate()
        for component in self.components:
            if component.type not in self.allowed_components:
                raise SemanticException(
                    "unexpected component {component} in {type}".format(component=component.type, type=self.type)
                )
            component.validate()
