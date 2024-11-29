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
    
    def __le__(self, other):
        return self.label.__le__(other.label)

    def __hash__(self):
        return hash(self.label)

    @staticmethod
    def join(vertex1, vertex2):
        # Should return a new VertexLabel that contains all pairs in both original Verticies.
        label1 = vertex1.label
        label2 = vertex2.label

        if (len(label1) == 0):
            return vertex2
        elif (len(label2) == 0):
            return vertex1
        
        index1 = 0
        index2 = 0
        result = []

        while (index1 < len(label1) and index2 < len(label2)):
            if (label1[index1][0][0] <= label2[index2][0][0]):
                result.append(label1[index1])
                index1 += 1
            else:
                result.append(label2[index2])
                index2 += 1
        
        while (index1 < len(label1)):
            result.append(label1[index1])
            index1 += 1
        while (index2 < len(label2)):
            result.append(label2[index2])
            index2 += 1
        
        return VertexLabel(tuple(result))