from Semantics import Semantics


class Reference(Semantics):
    entity_from = None
    entity_to = None
    union = None
    type = "Reference"
    required_attributes = ['name', 'references']
    optional_attributes = ['inverse']

    def build(self, entity, union=None):
        self.entity_from = entity
        self.union = union
        self.entity_to = entity.get_schema().find_entity(self.attributes['references'])
        self.entity_to.accept_referrer(self)

    def get_referrer_name(self):
        if 'inverse' in self.attributes:
            return self.attributes['inverse']
        return self.entity_from.get_name()

    def get_entity(self):
        return self.entity_from

    def get_referenced(self):
        return self.entity_to

    def is_union(self):
        return self.union is not None

    def get_union(self):
        return self.union
