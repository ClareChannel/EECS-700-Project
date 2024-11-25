"""
InputDataGraph class
Authors: Elizabeth Channel, Samuel Buehler
Description: Node-Edge-Based class based on BlinkFill and our Project Proposal.
Date Modified: 2024-11-23
"""

import re
import VertexLabel

class InputDataGraph:
    """
    InputDataGraph class
    """
    def __init__(self, inputString, index):
        """
        Creates an InputDataGraph based on the fresh input string and 
        the intersection of the graphs of all previous inputs.
        """
        self.vertices = set()
        self.edges = dict()
        self.patterns = set()
        self.rankedNodes = None
        self.__generate(inputString, index)

    def __generate(self, input, index):
        """
        Creates the graph for the graph's input.
        """
        # Create vertices
        for i in range(0, len(input) + 3):
            self.nodes.add(VertexLabel( ((index, i),) ))

        first = VertexLabel( ((index, 0),) )
        second = VertexLabel( ((index, 1),) )
        secondToLast = VertexLabel( ((index, len(input) +1),) )
        last = VertexLabel( ((index, len(input) + 2),) )
        # Set leftIdx and rightIdx
        self.edges[(first,second)] = {(-2, 1)}
        self.edges.setdefault((secondToLast, last), set())
        self.edges[(secondToLast, last)].add((-1, 1))
        self.patterns.update({(-2,1), (-1,1)})

        # Find all regex tokens within the input.
        regex_patterns = [
            r'\d+',         # Digits
            r'[()-]',       # Parentheses and hyphen
            r'\s+',         # Spaces
            r'[^\d\s()-]+'  # Any non-numeric, non-space, non-separator
        ]
        for pattern in regex_patterns:
            for match in re.finditer(pattern,input):
                start, end = match.start(), match.end()
                node = VertexLabel(((index, start), (index, end)))
                self.vertices.add(node)
                if len(self.vertices) > 1:
                    prevNode = list(self.vertices)[-2]
                    self.edges.setdefault((prevNode, node), set()).add((start, end - start))

    def __genSubStrExpr(self, input, leftIndex, rightIndex):
        # Generates set of substring expressions.
        pass

    def __rankNodes(self):
        # Assigns scores to the nodes of the InputDataGraph.
        self.rankedNodes = []

        for node in self.vertices:
            score = 0
            substr = str(node)
            # Assign score based on properties (ex: length, digit density)
            score += len(substr) # Substrings with larger lengths score higher
            score += sum(1 for c in substr if c.isdigit()) # Substrings with digits score higher
            self.rankedNodes.sort(key=lambda x: -x[1]) # Sort decending by score

    def intersect(self, secondGraph):
        # Find the intersection of the graph and the given secondGraph.
        newGraph = InputDataGraph("", 0)
        
        for node1 in self.vertices:
            for node2 in secondGraph.vertices:
                if node1 == node2:
                    newGraph.vertices.add(node1)
        for edge, patterns in self.edges.items():
            if edge in secondGraph.edges:
                newGraph.edges[edge] = self.edges[edge].intersection(secondGraph.edges[edge])
        return newGraph

    def getRegExes(self):
        regexes = []
        
        for node, score in self.rankedNodes:
            substr = str(node)

            regex = re.escape(substr)
            regexes.append(regex)
        return regexes

    def getDistance(self):
        pass
    
    def __str__(self):
        # Overloads str function to print a rough text form of the graph.
        pass