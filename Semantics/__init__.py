class Semantics:
    type = "*undefined*"
    required_attributes = ['name']
    optional_attributes = []
    name = None

    def __init__(self, attributes):
        self.attributes = attributes
        if 'name' in attributes:
            self.name = attributes['name']

    def __str__(self):
        return self.str(0)

    def str(self, depth):
        return self.pad(depth) + self.type + " " + str(self.attributes)

    def validate(self):
        for attribute in self.required_attributes:
            if attribute not in self.attributes:
                raise SemanticException(
                    "required attribute {attribute} for {type} not found".format(attribute=attribute, type=self.type)
                )
        for attribute in self.attributes:
            if attribute not in self.required_attributes and attribute not in self.optional_attributes:
                raise SemanticException(
                    "unrecognised attribute {attribute} for {type}".format(attribute=attribute, type=self.type)
                )

    def get_name(self):
        return self.attributes['name']

    @staticmethod
    def pad(depth):
        return " " * depth * 4


class SemanticException(Exception):
    pass

