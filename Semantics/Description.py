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


class Description(Semantics):
    type = "Description"

    def __init__(self, attrib, components, text):
        if len(attrib):
            raise SemanticException('description does not support attributes')
        if len(components):
            raise SemanticException('description can not contain components')
        super().__init__({})
        self.text = text

    def required_attributes(self):
        return []  # N.B no super() - override

    def __str__(self):
        return self.str(0)

    def str(self, depth):
        return self.pad(depth) + "Description " + self.text
