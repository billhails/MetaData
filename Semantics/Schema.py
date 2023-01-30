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
from Semantics.Association import Association
from Semantics.Container import Container
from Semantics.Entity import Entity


class Schema(Container):
    entities = {}
    associations = []
    type = "Schema"
    allowed_components = ['Entity', 'Association']

    def __init__(self, attributes, components):
        super().__init__(attributes, components)

    def optional_attributes(self):
        return super().optional_attributes() + [
            {'name': 'auth', 'values': ['enabled', 'disabled'], 'default': 'disabled'},
            {'name': 'access-token-expiry'},
            {'name': 'security', 'values': ['xss']}
        ]

    def build(self):
        self.entities = {x.attributes['name']: x for x in self.components if isinstance(x, Entity)}
        self.associations = [x for x in self.components if isinstance(x, Association)]
        for entity in self.entities:
            self.entities[entity].build(self)
        for association in self.associations:
            association.build(self)

    def validate(self):
        super().validate()
        if self.is_auth_enabled():
            self.validate_auth_role('owner')
            self.validate_auth_role('token')
            self.validate_auth_role('role')
            self.validate_auth_role_association()

    def validate_auth_role(self, role):
        found = False
        for entity in self.entities:
            if self.entities[entity].is_auth_role(role):
                if found:
                    raise SemanticException(f"duplicate entities with auth-role={role}")
                found = True
        if not found:
            raise SemanticException(f"schema has auth enabled but no entity with auth-role={role} was defined")

    def validate_auth_role_association(self):
        auth_owner = self.get_auth_owner_entity()
        auth_role = self.get_auth_role_entity()
        found = False
        for association in self.get_associations():
            if association.is_auth_role('role'):
                if found:
                    raise SemanticException('multiple associations with auth-role=role')
                found = True
                lhs = association.get_lhs()
                rhs = association.get_rhs()
                if not((lhs == auth_owner and rhs == auth_role) or (lhs == auth_role and rhs == auth_owner)):
                    raise SemanticException('auth role association does not connect owner to role')
        if not found:
            raise SemanticException('schema has auth enabled but no association with auth-role=role was defined')

    def find_entity(self, name):
        if name in self.entities:
            return self.entities[name]
        raise SemanticException(f"entity {name} not found in schema")

    def get_entities(self):
        return self.entities.values()

    def get_associations(self):
        return self.associations

    def is_auth_enabled(self):
        return self.attribute_value('auth', 'enabled')

    def is_xss_secure(self):
        return self.attribute_value('security', 'xss')

    def get_auth_owner_entity(self):
        for entity in self.get_entities():
            if entity.is_auth_role('owner'):
                return entity
        return None

    def get_auth_role_association(self):
        for association in self.get_associations():
            if association.is_auth_role('role'):
                return association
        return None

    def get_auth_token_entity(self):
        for entity in self.get_entities():
            if entity.is_auth_role('token'):
                return entity
        return None

    def get_auth_role_entity(self):
        for entity in self.get_entities():
            if entity.is_auth_role('role'):
                return entity
        return None

    def access_token_expiry(self):
        if 'access-token-expiry' in self.attributes:
            return self.attributes['access-token-expiry']
        return '1h'  # FIXME is this jwt-specific?
