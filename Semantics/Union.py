from Semantics.Container import Container


class Union(Container):
    type = "Union"
    required_attributes = ['name']
    allowed_components = ['Reference']

    def build(self, entity):
        for component in self.components:
            component.build(entity, self)

    def get_references(self):
        return self.components
