from Semantics import SemanticException
from Semantics.Container import Container
from Semantics.Description import Description
from Semantics.Field import Field
from Semantics.Reference import Reference
from Semantics.Union import Union


class Entity(Container):
    type = "Entity"
    required_attributes = ['name']
    allowed_components = ['Description', 'Field', 'Reference', 'Union']

    def __init__(self, attributes, components):
        super().__init__(attributes, components)
        self.schema = None
        self.description = None
        self.fields = {}
        self.references = {}
        self.unions = {}
        self.lhs_associations = {}
        self.rhs_associations = {}
        self.referrers = {}

    def build(self, schema):
        self.schema = schema
        self.fields = {x.attributes['name']: x for x in self.components if isinstance(x, Field)}
        self.references = {x.attributes['name']: x for x in self.components if isinstance(x, Reference)}
        self.unions = {x.attributes['name']: x for x in self.components if isinstance(x, Union)}
        self.description = [x.text for x in self.components if isinstance(x, Description)][0]
        for field in self.fields:
            self.fields[field].build(self)
        for reference in self.references:
            self.references[reference].build(self)
        for union in self.unions:
            self.unions[union].build(self)

    def get_fields(self):
        return self.fields.values()

    def get_references(self):
        return self.references.values()

    def get_unions(self):
        return self.unions.values()

    def get_referrers(self):
        return self.referrers.values()

    def get_schema(self):
        return self.schema

    def get_description(self):
        return self.description

    def accept_rhs_association(self, association):
        self.rhs_associations[association.get_name()] = association

    def accept_lhs_association(self, association):
        self.lhs_associations[association.get_name()] = association

    def accept_referrer(self, reference):
        name = reference.get_referrer_name()
        if name in self.referrers:
            raise SemanticException(
                "duplicate reference {name} from {a} and {b} to {this}, consider declaring an inverse attribute".format(
                    name=name,
                    a=self.referrers[name].get_entity().get_name(),
                    b=reference.get_entity().get_name(),
                    this=self.get_name()
                )
            )
        self.referrers[name] = reference
