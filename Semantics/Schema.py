from Semantics import SemanticException
from Semantics.Association import Association
from Semantics.Container import Container
from Semantics.Entity import Entity


class Schema(Container):
    entities = {}
    associations = []
    type = "Schema"
    required_attributes = ['name']
    allowed_components = ['Entity', 'Association']

    def __init__(self, attributes, components):
        super().__init__(attributes, components)

    def build(self):
        self.entities = {x.attributes['name']: x for x in self.components if isinstance(x, Entity)}
        self.associations = [x for x in self.components if isinstance(x, Association)]
        for entity in self.entities:
            self.entities[entity].build(self)
        for association in self.associations:
            association.build(self)

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
