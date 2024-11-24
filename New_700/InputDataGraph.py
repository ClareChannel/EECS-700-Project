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
        self.edges[(first, second)] = set()
        self.edges[(first,second)].add((-2,1))
        self.edges.setdefault((secondToLast, last), set())
        self.edges[(secondToLast, last)].add((-1, 1))
        self.patterns.add((-2, 1))
        self.patterns.add((-1, 1))

        # Find all regex tokens within the input.


    def __genSubStrExpr(self, input, leftIndex, rightIndex):
        # Generates set of substring expressions.
        pass

    def __rankNodes(self):
        # Assigns scores to the nodes of the InputDataGraph.
        pass

    def intersect(self, secondGraph):
        # Find the intersection of the graph and the given secondGraph.
        pass

    def getRegExes(self):
        pass

    def getDistance(self):
        pass
    
    def __str__(self):
        # Overloads str function to print a rough text form of the graph.
        pass