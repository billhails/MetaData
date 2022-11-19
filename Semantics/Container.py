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
