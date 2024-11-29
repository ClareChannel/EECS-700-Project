from bisect import bisect_left

class VertexLabel:
    """
    VertexLabel is the label of a DAG node.
    """

    def __init__(self, label):
        self.label = tuple(sorted(label))

    def __str__(self):
        # Include substring in debug output if available
        '''if len(self.label) == 3:
            return f"Substring: '{self.label[2]}' at {self.label[:2]}"
        return str(self.label)'''
        return f"Substr: {self.label}"

    def __eq__(self, other):
        return isinstance(other, VertexLabel) and self.label == other.label
    
    def __lt__(self, other):
        return self.label < other.label

    def __hash__(self):
        return hash(self.label)
        
    def __getitem__(self, ind):
        ids, inds = zip(*self.label) if self.label else ([], [])
        pos = bisect_left(ids, ind)
        return inds[pos] if pos < len(ids) and ids[pos] == ind else None

    def ids(self):
        return tuple(zip(*self.label))
    
    def inds(self):
        return tuple(zip(*self.label))

    @staticmethod
    def join(vertex1, vertex2):
        # Should return a new VertexLabel that contains all pairs in both original Verticies.
        return VertexLabel(sorted(vertex1.label + vertex2.label))