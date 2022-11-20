from Semantics import Semantics


class Association(Semantics):
    type = "Association"
    lhs = None
    rhs = None
    schema = None
    required_attributes = ['name', 'lhs', 'rhs']
    self_referential = None

    def build(self, schema):
        self.schema = schema
        self.lhs = schema.find_entity(self.attributes['lhs'])
        self.rhs = schema.find_entity(self.attributes['rhs'])
        self.lhs.accept_lhs_association(self)
        self.rhs.accept_rhs_association(self)
        self.self_referential = (self.lhs == self.rhs)

    def get_lhs(self):
        return self.lhs

    def get_rhs(self):
        return self.rhs

    def get_name_for_other_entity(self, entity):
        if self.self_referential:
            return self.get_name()
        if entity == self.lhs:
            return self.rhs.get_name()
        return self.lhs.get_name()

    def get_other(self, entity):
        if entity == self.lhs:
            return self.rhs
        return self.lhs

    def get_lhs_column(self):
        return self.lhs.get_name() + '_lhs_id'

    def get_rhs_column(self):
        return self.rhs.get_name() + '_rhs_id'

    def get_this_column(self, entity):
        if entity == self.lhs:
            return self.get_lhs_column()
        return self.get_rhs_column()

    def get_other_column(self, entity):
        if entity == self.lhs:
            return self.get_rhs_column()
        return self.get_lhs_column()

    def is_self_referential(self):
        return self.self_referential
