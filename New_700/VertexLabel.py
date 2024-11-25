class VertexLabel:
    """
    VertexLabel is the label of a Dag node.
    """

    def __init__(self, label):
        self.label = label

    def __str__(self):
        return str(self.label)