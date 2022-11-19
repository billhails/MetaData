from Semantics import Semantics


class Association(Semantics):
    type = "Association"
    lhs = None
    rhs = None
    schema = None
    required_attributes = ['name', 'lhs', 'rhs']

    def build(self, schema):
        self.schema = schema
        self.lhs = schema.find_entity(self.attributes['lhs'])
        self.rhs = schema.find_entity(self.attributes['rhs'])
        self.lhs.accept_lhs_association(self)
        self.rhs.accept_rhs_association(self)

    def get_lhs(self):
        return self.lhs

    def get_rhs(self):
        return self.rhs