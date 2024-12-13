class VertexLabel:
    """
    VertexLabel is the label of a DAG node.
    """

    def __init__(self, label):
        self.label = label

    def __str__(self):
        # Include substring in debug output if available
        if len(self.label) == 3:
            return f"Substring: '{self.label[2]}' at {self.label[:2]}"
        return str(self.label)

    def __eq__(self, other):
        return isinstance(other, VertexLabel) and self.label == other.label

    def __hash__(self):
        return hash(self.label)

