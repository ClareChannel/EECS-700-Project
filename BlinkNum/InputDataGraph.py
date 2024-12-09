# BlinkFill paper functions not included in this class:
# GenerateDag(), GenSubStrExpr(), LearnProgram(), TopRankExpr()
# Some of these excluded functions may be useful to put in this class, rather than in another class.

class InputDataGraph:
    def __init__(self, inStr):
        self.vertices = set()
        #self.edges = set()
        self.edges = {}
        #self.patterns = set()
        #self.ranked = None
        self.I = {}
        self.L = {}
        self.__GenerateInputGraph(inStr)
    
    """
    def __GenerateInputGraph(self, inStr):
        # TODO: Generate an ID?
        for i in range(0, len(inStr) + 3):
            self.vertices = self.vertices.union(self.vertices[i])
            # I[i] = { (id, i) }
        # L.add( { self.vertices[0], self.vertices[1], {'^','1'} } )
        for i in range(1, len(inStr) + 1):
            for j in range(i+1, len(inStr) + 2):
                leftIdx = i, rightIdx = j-1
                self.edges = self.edges.union(self.vertices[i], self.vertices[j]) # Should edges be a dict?
                constantString = inStr[leftIdx:rightIdx]
                #L( (self.vertices[i], self.vertices[j]) ) = { (constantString, GetMId(constantString, inStr, i)) } # I still don't recall what this is supposed to do.
                '''
                # TODO: This still needs to be comprehended so it can be properly finished!
                for r in T and Match(r, constantString):
                    L( (self.vertices[i], self.vertices[j]) ) = L( (self.vertices[i], self.vertices[j]) ).union(r, GetMId(r,inStr,i))
                '''
        # L.add = { self.vertices[len(inStr) + 1], self.vertices[len(inStr) = 2], {'$','1'} }
    """
    def __GenerateInputGraph(self, inStr):
        strLen = len(inStr)
        strId = hash(inStr) # Generates a unique ID for the given input string

        # Create vertices for each character index and boundary nodes
        for i in range(strLen + 1):
            self.vertices.add(i)
            self.I[i] = (strId, i) # Map vertex to string ID and index

        # Create edges between the vertices representing substrings
        for i in range(strLen):
            for j in range(i + 1, strLen + i):
                self.edges[(i, j)] = inStr[i:j] # Label edge with the substring

    def Rank_Verts(self):
        scores = {v: 0 for v in self.vertices}
        for (start, end), label in self.edges.items():
            distance = abs(self.I[end][1] - self.I[start][1])
            scores[start] += distance
            scores[end] += distance
        return sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    def __repr__(self):
        return f"InputDataGraph(vertices={self.vertices}, edges={self.edges})"

    def GenInpDataGraph(self, columns):
        """
        First constructs a graph for each column, then returns the union of these graphs.

        Input: Set of all input rows (n), each for k columns/strings.
        Output: Post-union graph.
        """
        graph = set()
        k = len(columns[0])
        for i in range(0, k):
            graph = graph.union(self.__GenGraphColumn(columns[i]))
        return graph

    def __GenGraphColumn(self, inp):
        """
        
        Input: Set of strings for each row.
        Output: InputDataGraph
        """
        graph = self.__GenerateInputGraph(inp[0]) # ...?
        n = len(inp)
        for i in range(1, n):
            graph = self.Intersect(graph, self.__GenerateInputGraph(inp[i]))
        return graph

    def RankInpGNodes(self):
        """
        
        """
        for vertex in self.vertices:
            vertex.out = 0
            vertex.inp = 0
            vertex.score = 0
        for vertex in self.vertices: # TODO: put the vertices in topological order
            for edge in self.edges:
                edge.vertex1.out = max(edge.vertex2.out + self.NodeDistance(edge.vertex1, edge.vertex2))
        for v in self.vertices: # TODO: put the vertices in reverse topolgical order
            for edge in self.edges:
                edge.vertex1.inp = max(edge.vertex1.inp, edge.vertex2.inp + self.NodeDistance(edge.vertex2, edge.vertex1))
        for vertex in self.vertices:
            vertex.score = vertex.inp + vertex.out
        # TODO: We could either return the vertex with the highest score, or we could use the self.ranked to a list of the vertices in order and then add a function to get the highest ranked node.

    def NodeDistance(self, vertex1, vertex2):
        """
        Python translation of the following psuedocode:
        phi_eta(vertex1, vertex2) = sum_(id in I(vertex1)) abs(vertex2[id] - vertex1[id])

        Inputs: Two vertices (vertex1, vertex2) and an InputDataGraph's set of vertex labels (I).
        Output: The sum of the equation.
        """
        ret = 0
        for id in I[vertex1]: # TODO: Need to clarify what I is.
            ret += abs(vertex2.id - vertex1.id)
        return ret

    def Intersect(self, graph1, graph2):
        """
        Inputs: Two InputDataGraphs, graph1 and graph 2.
        Outputs: InputDataGraph graph
        """
        # NOTE: This function may need to be moved to a generalized class (i.e. main).

        # TODO: For Intesect, check if disjoint first, then merge/intersect.
        graph = InputDataGraph('')
        graph.vertices = graph1.vertices.intersection(graph2.vertices)
        graph.edges = graph1.edges.intersection(graph2.edges)
        # TODO: I?
        # TODO: L?
        return graph