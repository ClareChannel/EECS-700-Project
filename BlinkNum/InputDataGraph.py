import re

TOKENS = [re.compile("\d+"),
            re.compile("[a-zA-Z]+"),
            re.compile("\s+"),
            re.compile("[A-Z][a-z]+"),
            re.compile("[A-Z]+"),
            re.compile("[a-z]+"),
            re.compile("[a-zA-Z0-9]+"),
            re.compile("[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*"),
            re.compile("[A-Z]+(?:\s+[A-Z]+)*"),
            re.compile("[a-z]+(?:\s+[a-z]+)*"),
            re.compile("[a-zA-Z]+(?:\s+[a-zA-Z]+)*")
        ]

class InputDataGraph:
    def __init__(self, inStr):
        self.vertices = set()
        self.edges = {}
        self.I = {}
        self.L = {}
        self.__GenerateInputGraph(inStr)
    
    def __GenerateInputGraph(self, inStr):
        """

        Input: input string
        Output: none (Entirely changes the self IDG)
        """
        id = hash(inStr)
        for i in range(0, len(inStr) + 3):
            self.vertices = self.vertices.union(self.vertices[i])
            self.I[i] = { (id, i) }
        
        self.L[ (self.vertices[0], self.vertices[1]) ] = { ('^','1') } # Create the first label
        self.L[ (self.vertices[len(inStr)] + 1, self.vertices[len(inStr) + 2]) ] = { ('$','1') } # Create the last label

        for i in range(1, len(inStr) + 1):
            for j in range(i+1, len(inStr) + 2):
                leftIdx = i, rightIdx = j-1
                self.edges = self.edges.union(self.vertices[i], self.vertices[j])
                constStr = inStr[leftIdx:rightIdx]
                self.L[ (self.vertices[i], self.vertices[j]) ] = { (constStr, hash(constStr, inStr, i)) }
                for token in TOKENS and re.match(token, constStr):
                    self.L[ (self.vertices[i], self.vertices[j]) ] = self.L[ (self.vertices[i], self.vertices[j] )].union(token, hash(token, inStr, i))

    def Rank_Verts(self):
        scores = {v: 0 for v in self.vertices}
        for (start, end), label in self.edges.items():
            distance = abs(self.I[end][1] - self.I[start][1])
            scores[start] += distance
            scores[end] += distance
        return sorted(scores.items(), key=lambda item: item[1], reverse=True)

    def GenInpDataGraph(self, columns):
        """
        First constructs a graph for each column, then returns the union of these graphs.

        Input: Set of all input rows (n), each for k columns/strings.
        Output: Post-union graph.
        """
        graphs = [] # Holds all of the graphs

        k = len(columns[0])

        
        for i in range(0, k):
            graph = graphs.append(self.__GenGraphColumn(columns[i]))
        
        #unionedGraph # Could just union these to the main IDG?

        return graph

    def __GenGraphColumn(self, inp):
        """
        
        Input: Set of strings for each row.
        Output: InputDataGraph
        """
        graph = self.__GenerateInputGraph(inp[0])
        n = len(inp)
        for i in range(1, n):
            graph = self.Intersect(graph, self.__GenerateInputGraph(inp[i])) # Should not use IDG, just IG
        return graph

    def RankInpGNodes(self):
        """
        Ranks each vertex based on node distances.
        Output: Vertex with the highest score
        """
        for vertex in self.vertices:
            vertex.out = 0
            vertex.inp = 0
            vertex.score = 0
        for vertex in self.vertices: # TODO: put the vertices in topological order (v, vi)
            for edge in self.edges:
                edge.vertex1.out = max(edge.vertex2.out + self.NodeDistance(edge.vertex1, edge.vertex2))
        for v in self.vertices: # TODO: put the vertices in reverse topolgical order (vi, v)
            for edge in self.edges:
                edge.vertex1.inp = max(edge.vertex1.inp, edge.vertex2.inp + self.NodeDistance(edge.vertex2, edge.vertex1))
        for vertex in self.vertices:
            vertex.score = vertex.inp + vertex.out
        
        # TODO: Need to return the vertex with the highest score

    def NodeDistance(self, vertex1, vertex2):
        """
        Python translation of the following psuedocode:
        phi_eta(vertex1, vertex2) = sum_(id in I(vertex1)) abs(vertex2[id] - vertex1[id])

        Inputs: Two vertices (vertex1, vertex2) and an InputDataGraph's set of vertex labels (I).
        Output: The sum of the equation.
        """
        ret = 0
        for id in self.I[vertex1]:
            ret += abs(vertex2.id - vertex1.id)
        return ret

    def Intersect(self, graph1, graph2):
        """
        Inputs: Two InputDataGraphs, graph1 and graph 2.
        Outputs: InputDataGraph graph
        """
        # NOTE: Professor's thought: For Intesect, check if disjoint first, then merge/intersect.
        graph = InputDataGraph('')
        graph.vertices = graph1.vertices.intersection(graph2.vertices)
        graph.edges = graph1.edges.intersection(graph2.edges)
        graph.I = graph1.I | graph2.I
        graph.L = graph1.L | graph2.L
        return graph