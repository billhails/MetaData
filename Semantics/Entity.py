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
from Semantics import SemanticException
from Semantics.Container import Container
from Semantics.Description import Description
from Semantics.Field import Field
from Semantics.Reference import Reference
from Semantics.Union import Union


class Entity(Container):
    type = "Entity"
    allowed_components = ['Description', 'Field', 'Reference', 'Union']

    def __init__(self, attributes, components):
        super().__init__(attributes, components)
        self.schema = None
        self.description = None
        self.fields = {}
        self.references = {}
        self.unions = {}
        self.lhs_associations = {}
        self.rhs_associations = {}
        self.all_associations = {}
        self.referrers = {}

    def optional_attributes(self):
        return super().optional_attributes() + ['auth-role']

    def build(self, schema):
        self.schema = schema
        self.fields = {x.attributes['name']: x for x in self.components if isinstance(x, Field)}
        self.references = {x.attributes['name']: x for x in self.components if isinstance(x, Reference)}
        self.unions = {x.attributes['name']: x for x in self.components if isinstance(x, Union)}
        self.description = [x.text for x in self.components if isinstance(x, Description)][0]
        for field in self.fields:
            self.fields[field].build(self)
        for reference in self.references:
            self.references[reference].build(self)
        for union in self.unions:
            self.unions[union].build(self)

    def validate(self):
        super().validate()
        self.validate_attribute('auth-role', ['user'])
        if self.is_auth_role('user'):
            got_id = False
            got_password = False
            for field in self.get_fields():
                if field.is_auth_role('external-id'):
                    if got_id:
                        raise SemanticException("duplicate declarations of auth-role=id")
                    got_id = True
                if field.is_auth_role('password'):
                    if got_password:
                        raise SemanticException("duplicate declaration for auth-role=password")
                    got_password = True
            if not got_id:
                raise SemanticException(
                    "entity {name} declared as auth-role=user but contains no field with auth-role=id".format(
                        name=self.name
                    )
                )
            if not got_password:
                raise SemanticException(
                    "entity {name} declared as auth-role=user but contains no field with auth-role=password".format(
                        name=self.name
                    )
                )

    def get_auth_id_field(self):
        for field in self.get_fields():
            if field.is_auth_role('external-id'):
                return field
        return None

    def get_auth_password_field(self):
        for field in self.get_fields():
            if field.is_auth_role('password'):
                return field
        return None

    def get_fields(self):
        return self.fields.values()

    def get_references(self):
        return self.references.values()

    def get_unions(self):
        return self.unions.values()

    def get_referrers(self):
        return self.referrers.values()

    def get_schema(self):
        return self.schema

    def get_description(self):
        return self.description

    def accept_rhs_association(self, association):
        self.rhs_associations[association.get_name()] = association
        self.all_associations[association.get_name()] = association

    def accept_lhs_association(self, association):
        self.lhs_associations[association.get_name()] = association
        self.all_associations[association.get_name()] = association

    def get_associations(self):
        return self.all_associations.values()

    def accept_referrer(self, reference):
        name = reference.get_referrer_name()
        if name in self.referrers:
            raise SemanticException(
                "duplicate reference {name} from {a} and {b} to {this}, consider declaring an inverse attribute".format(
                    name=name,
                    a=self.referrers[name].get_entity().get_name(),
                    b=reference.get_entity().get_name(),
                    this=self.get_name()
                )
            )
        self.referrers[name] = reference
