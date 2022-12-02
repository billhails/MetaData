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
            {'name': 'access-token-expiry'}
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
            found_user_auth = False
            found_token_auth = False
            for entity in self.entities:
                if self.entities[entity].is_auth_role('owner'):
                    if found_user_auth:
                        raise SemanticException("duplicate entities with auth-role=owner")
                    found_user_auth = True
                if self.entities[entity].is_auth_role('token'):
                    if found_token_auth:
                        raise SemanticException('duplicate entities with auth-role=token')
                    found_token_auth = True
            if not found_user_auth:
                raise SemanticException("schema has auth enabled but no entity with auth-role=owner was defined")
            if not found_token_auth:
                raise SemanticException('schema has auth enabled but no entity with auth-role=token was defined')

    def find_entity(self, name):
        if name in self.entities:
            return self.entities[name]
        raise SemanticException(
            "entity {name} not found in schema".format(name=name)
        )

    def get_entities(self):
        return self.entities.values()

    def get_associations(self):
        return self.associations

    def is_auth_enabled(self):
        return self.attribute_value('auth', 'enabled')

    def get_auth_owner_entity(self):
        for entity in self.get_entities():
            if entity.is_auth_role('owner'):
                return entity
        return None

    def get_auth_token_entity(self):
        for entity in self.get_entities():
            if entity.is_auth_role('token'):
                return entity
        return None

    def access_token_expiry(self):
        if 'access-token-expiry' in self.attributes:
            return self.attributes['access-token-expiry']
        return '1h'  # FIXME is this jwt-specific?
