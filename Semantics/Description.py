from Semantics import Semantics


class Description(Semantics):
    type = "Description"
    required_attributes = []

    def __init__(self, text):
        super().__init__({})
        self.text = text


    def __str__(self):
        return self.str(0)

    def str(self, depth):
        return self.pad(depth) + "Description " + self.text
