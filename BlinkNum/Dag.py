class DAG:
    def __init__(self, outStr):
        self.nodes = list(range(len(outStr) + 1))
        self.edges = {}
    
    def addEdge(self, start, end, label):
        if (start, end) not in self.edges:
            self.edges[(start, end)] = []
        self.edges[(start, end)].append(label)

    def __repr__(self):
        return f"DAG(nodes={self.nodes}, edges={self.edges})"