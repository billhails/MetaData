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


class Association(Semantics):
    type = "Association"
    lhs = None
    rhs = None
    schema = None
    self_referential = None

    def required_attributes(self):
        return super().required_attributes() + [
            {'name': 'lhs'},
            {'name': 'rhs'}
        ]

    def optional_attributes(self):
        return super().optional_attributes() + [
            {'name': 'auth-access', 'values': ['any', 'owner', 'admin'], 'default': 'any'},
            {'name': 'auth-path'},
            {'name': 'auth-visibility', 'values': ['visible', 'hidden'], 'default': 'visible'}
        ]

    def build(self, schema):
        self.schema = schema
        self.lhs = schema.find_entity(self.attributes['lhs'])
        self.rhs = schema.find_entity(self.attributes['rhs'])
        self.lhs.accept_lhs_association(self)
        self.rhs.accept_rhs_association(self)
        self.self_referential = (self.lhs == self.rhs)

    def get_lhs(self):
        return self.lhs

    def get_rhs(self):
        return self.rhs

    def get_name_for_other_entity(self, entity):
        if self.self_referential:
            return self.get_name()
        if self.is_lhs(entity):
            return self.rhs.get_name()
        return self.lhs.get_name()

    def get_other(self, entity):
        if self.is_lhs(entity):
            return self.rhs
        return self.lhs

    def get_lhs_column(self):
        return self.lhs.get_name() + '_lhs_id'

    def get_rhs_column(self):
        return self.rhs.get_name() + '_rhs_id'

    def get_this_column(self, entity):
        if self.is_lhs(entity):
            return self.get_lhs_column()
        return self.get_rhs_column()

    def get_other_column(self, entity):
        if self.is_lhs(entity):
            return self.get_rhs_column()
        return self.get_lhs_column()

    def is_self_referential(self):
        return self.self_referential

    def is_lhs(self, entity):
        return entity == self.lhs
