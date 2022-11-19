from Semantics import Semantics, SemanticException


class Field(Semantics):
    entity = None
    type = "Field"
    required_attributes = ['name', 'type']
    known_types = [
        "string",
        "guid",
        "small_string"
    ]

    def build(self, entity):
        self.entity = entity

    def get_type(self):
        return self.attributes['type']

    def get_entity(self):
        return self.entity

    def validate(self):
        super().validate()
        if self.get_type() not in self.known_types:
            raise SemanticException(
                "unrecognised type {type} for field {entity}.{name}".format(
                    type=self.get_type(),
                    entity=self.get_entity().get_name(),
                    name=self.get_name()
                )
            )
