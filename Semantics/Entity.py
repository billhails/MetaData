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
from Semantics.Description import Description
from Semantics.Field import Field
from Semantics.Reference import Reference
from Semantics.Union import Union
from Semantics.ID import ID
from Semantics.Enum import Enum

class Entity(Container):
    """
    This class represents <entity> elements and their contents
    """

    type = "Entity"
    allowed_components = ['Description', 'Field', 'Reference', 'Union', 'Enum']

    def __init__(self, attributes, components):
        super().__init__(attributes, components)
        self.schema = None
        self.description = None
        self.fields = {}
        self.references = {}
        self.unions = {}
        self.enums = {}
        self.lhs_associations = {}
        self.rhs_associations = {}
        self.all_associations = {}
        self.referrers = {}

    def optional_attributes(self):
        return super().optional_attributes() + [
            {'name': 'auth-role', 'values': ['owner', 'token', 'role', 'none'], 'default': 'none'},
            {'name': 'auth-access', 'values': ['any', 'owner', 'admin'], 'default': 'any'},
            {'name': 'auth-visibility', 'values': ['visible', 'hidden'], 'default': 'visible'},
            {'name': 'debug', 'default': 'none'}
        ]

    def build(self, schema):
        self.schema = schema
        self.fields = {x.attributes['name']: x for x in self.components if isinstance(x, Field)}
        self.references = {x.attributes['name']: x for x in self.components if isinstance(x, Reference)}
        self.unions = {x.attributes['name']: x for x in self.components if isinstance(x, Union)}
        self.enums = {x.attributes['name']: x for x in self.components if isinstance(x, Enum)}
        self.description = [x.text for x in self.components if isinstance(x, Description)][0]
        for field in self.fields:
            self.fields[field].build(self)
        for reference in self.references:
            self.references[reference].build(self)
        for union in self.unions:
            self.unions[union].build(self)
        for enum in self.enums:
            self.enums[enum].build(self)

    def validate(self):
        super().validate()
        self.validate_auth_fields('owner', ['external-id', 'password'])
        self.validate_auth_fields('token', ['token'])
        self.validate_auth_references('token', ['owner'])
        self.validate_components()

    def has_auth_role(self):
        return self.has_attribute_not('auth-role', 'none')

    def has_auth_owner(self):
        for reference in self.get_references():
            if reference.is_auth_role('owner'):
                return True
        return False

    def validate_auth_fields(self, entity_role, field_roles):
        self.validate_auth_components(entity_role, field_roles, self.get_fields())

    def validate_auth_references(self, entity_role, reference_roles):
        self.validate_auth_components(entity_role, reference_roles, self.get_references())

    def validate_auth_components(self, entity_role, component_roles, components):
        if self.is_auth_role(entity_role):
            for component_role in component_roles:
                found = False
                for component in components:
                    if component.is_auth_role(component_role):
                        if found:
                            raise SemanticException(
                                "duplicate declarations of auth-role={role} for entity {name}".format(
                                    role=component_role,
                                    name=self.get_name()
                                )
                            )
                        found = True
                if not found:
                    raise SemanticException(
                        f'entity {self.get_name()} declared as auth-role={entity_role} but contains no component with '
                        f'auth-role={component_role}'
                    )

    def validate_components(self):
        for component in self.components:
            component.validate()

    def has_only_auth_components(self):
        for field in self.get_fields():
            if not field.is_auth():
                return False
        return True

    def get_auth_id_field(self):
        return self.get_auth_field('external-id');

    def get_auth_field(self, role):
        for field in self.get_fields():
            if field.is_auth_role(role):
                return field
        raise SemanticException(f'entity {self.get_name()} has no field with auth-role={role}')

    def get_auth_password_field(self):
        return self.get_auth_field('password')

    def get_auth_owner_reference(self):
        for reference in self.get_references():
            if reference.is_auth_role('owner'):
                return reference
        return ID({"name": 'id'})

    def get_auth_token_field(self):
        return self.get_auth_field('token')

    def get_auth_reference(self, role):
        for reference in self.get_references():
            if reference.is_auth_role(role):
                return reference
        raise SemanticException(f'entity {self.get_name()} has no reference with auth-role={role}')

    def get_field_with_type(self, field_type):
        for field in self.get_fields():
            if field.get_type() == field_type:
                return field
        return None

    def get_fields(self):
        return self.fields.values()

    def get_unique_fields(self):
        return [field for field in self.get_fields() if field.is_unique()]

    def get_references(self):
        return self.references.values()

    def has_references(self):
        return len(self.get_references()) > 0

    def get_unions(self):
        return self.unions.values()

    def has_unions(self):
        return len(self.get_unions()) > 0

    def get_referrers(self):
        return self.referrers.values()

    def get_enums(self):
        return self.enums.values()

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

    def is_auth_enabled(self):
        return self.get_schema().is_auth_enabled()

    def is_debug(self, debug):
        return self.attribute_value('debug', debug)