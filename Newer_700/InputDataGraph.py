"""
InputDataGraph class
Authors: Elizabeth Channel, Samuel Buehler
Description: Node-Edge-Based class based on BlinkFill and our Project Proposal.
Date Modified: 2024-11-23
"""

import re
from VertexLabel import VertexLabel
from Tokens import TOKENS
from copy import copy

from collections import defaultdict, deque

def topSort(vertices, keys):
    indegree = defaultdict(int)
    adjList = defaultdict(list)

    for source, dest in keys:
        indegree[dest] += 1
        adjList[source].append(dest)
    
    queue = deque([vertex for vertex in vertices if indegree[vertex] == 0])
    topSort = []

    while queue:
        vertex = queue.popleft()
        topSort.append(vertex)
        for neighbor in adjList[vertex]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    return topSort

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
        Creates the graph for the input string.
        """
        '''prevNode = None
        regex_patterns = [
            r'\d+',         # Digits
            r'[()-]',       # Parentheses and hyphen
            r'\s+',         # Spaces
            r'[^\d\s()-]+'  # Any non-numeric, non-space, non-separator
        ]
        for pattern in regex_patterns:
            for match in re.finditer(pattern, input):
                start, end = match.start(), match.end()
                substr = input[start:end]
                node = VertexLabel(((index, start), (index, end), substr))
                self.vertices.add(node)
                if prevNode:
                    self.edges.setdefault((prevNode, node), set()).add((start, end - start))
                prevNode = node
                print(f"Created node: {node}")
            print(f"Found pattern: {pattern}")


        # Debugging vertices and edges
        print("\n--- Debugging Node and Edge Generation ---")
        print("Vertices:")
        for vertex in self.vertices:
            print(f"  {vertex}")
        print("Edges:")
        for edge, patterns in self.edges.items():
            print(f"  {edge[0]}, {edge[1]}: {patterns}")
        print("--- End of Node and Edge Generation ---\n")'''
        num_verts = len(input) + 3

        for i in range(num_verts): # Create vertices
            self.vertices.add(VertexLabel(((index, i),)))
        
        firstVert = VertexLabel(((index, 0),))
        secondVert = VertexLabel(((index, 1),))
        secondToLastVert = VertexLabel(((index, len(input) + 1),))
        lastVert = VertexLabel(((index, len(input) + 2),))

        # Set start and end edges
        self.edges.setdefault((firstVert, secondVert), set()).add((-2, 1))
        self.edges.setdefault((secondToLastVert, lastVert), set()).add((-1, 1))
        self.patterns.update({(-2, 1), (-1, 1)})

        #
        for i, tokens in enumerate(TOKENS):
            matches = list(tokens.finditer(input))
            totalMatches = len(matches)

            for ind, match in enumerate(matches, start=1):
                start = VertexLabel(((index, match.start() + 1),))
                end = VertexLabel(((index, match.end() + 1),))
                label = (start, end)

                # Add positive and negative match indices
                self.edges.setdefault(label, set()).update({
                    (i, ind),
                    (i, ind - totalMatches - 1)
                })
                self.patterns.update({
                    (i, ind),
                    (i, ind - totalMatches - 1)
                })
        
        # Add constant labels
        for i in range(1, len(input) + 1):
            for j in range (i + 1, len(input) + 2):
                start = VertexLabel(((index, i),))
                end = VertexLabel(((index, j),))
                label = (start, end)
                constStr = input[i - 1: j - 1]

                # Compute matching indicies
                constMatch = re.compile(re.escape(constStr))
                ind = len(constMatch.findall(input[:i - 1 + len(constStr)]))
                negInd = -len(constMatch.findall(input[i - 1:]))

                self.edges.setdefault(label, set()).update({
                    (constStr, ind),
                    (constStr, negInd)
                })
                self.patterns.update({
                    (constStr, ind),
                    (constStr, negInd)
                })

    def __str__(self):
        # Format vertices
        vertStr = "set(" + ", ".join(str(n) for n in self.vertices) + ")"
        ret = "vertices: " + vertStr

        # Format edges
        for k, edgeVals in self.edges.items():
            edgeList = ", ".join(
                f' ({"\"" + re + "\"" if isinstance(re, str) else TOKENS[re]}, {num})'
                for re, num in edgeVals
            )
            ret += f"\n{str(k[0])} to {str(k[1])}: {{{edgeList}}}"

        return ret

#Incorporating positional penalties or rewards based on node adjacency 
# and known phone number structures
    def rankNodes(self):
        """
        Assigns scores to nodes based on their relevance to phone numbers.
        """
        '''self.rankedNodes = []

        for node in self.vertices:
            if isinstance(node.label, tuple) and len(node.label) == 3:
                substr = node.label[2]  # Extract the substring
                score = 0

                # Prioritize digits and separators
                if re.match(r'^\d+$', substr):  # Digits
                    score += 10
                elif re.match(r'^[-.()\s]+$', substr):  # Separators
                    score += 5

                # Penalize single-character substrings unless they are separators
                if len(substr) == 1 and not re.match(r'^[-.()\s]$', substr):
                    score -= 2

                # Add nodes with a positive score
                if score > 0:
                    self.rankedNodes.append((node, score))

        # Sort nodes by descending score
        self.rankedNodes.sort(key=lambda x: -x[1])
        print(f"Ranked Nodes: {[str(n[0]) for n in self.rankedNodes]}")'''
        vIn = {v: 0 for v in self.vertices}
        vOut = {v: 0 for v in self.vertices}
        vScore = {v: 0 for v in self.vertices}

        sortedVerts = topSort(self.vertices, self.edges.keys())

        for v in sortedVerts:
            for key in self.edges.keys():
                if key[0] == v:
                    distance = InputDataGraph.vertDistance(key[0], key[1])
                    vOut[v] = max(vOut[v], vOut[key[1]] + distance)
        
        for v in reversed(sortedVerts):
            for key in self.edges.keys():
                if key[1] == v:
                    distance = InputDataGraph.vertDistance(key[0], key[1])
                    vIn[v] = max(vIn[v], vIn[key[0]] + distance)
        
        vScore = {v: vIn[v] + vOut[v] for v in self.vertices}

        self.rankedNodes = {k: score for score, k in sorted(vScore.items(), key=lambda item: -item[1])}

#combining regex patterns directly
    def intersect(self, secondGraph):
        """
        Find the intersection of the graph with another graph.
        TODO: Make this work and actually use it.
              Might require (or at least be helpful to have) a working and legible
              "print IDG" function.
        """
        '''newGraph = InputDataGraph("", 0)

        for node1 in self.vertices:
            for node2 in secondGraph.vertices:
                if node1 == node2:
                    newGraph.vertices.add(node1)

        for edge, patterns in self.edges.items():
            if edge in secondGraph.edges:
                newGraph.edges[edge] = self.edges[edge].intersection(secondGraph.edges[edge])

        print(f"Intersected Graph Nodes: {newGraph.vertices}")
        return newGraph'''
        temp: InputDataGraph = copy(self)
        newVerts = set()
        newEdges = dict()
        newPatterns = set()

        for selfEdgeKey in self.edges.keys():
            for secondEdgeKey in secondGraph.edges.keys():
                common = set.intersection(self.edges[selfEdgeKey], secondGraph.edges[secondEdgeKey])
                if common:
                    vertex1 = VertexLabel.join(secondEdgeKey[0], secondEdgeKey[0])
                    vertex2 = VertexLabel.join(secondEdgeKey[1], secondEdgeKey[1])
                    newVerts.add(vertex1)
                    newVerts.add(vertex2)
                    newEdges[(vertex1, vertex2)] = common
                    newPatterns = newPatterns.union(common)
        temp.edges = newEdges
        temp.vertices = newVerts
        temp.patterns = newPatterns
        return temp

#Generate multiple regex fragments
#attempt to merge overlapping patterns

    def getRegExes(self):
        """
        Generate regex patterns by generalizing substrings from ranked nodes.
        """
        if not self.rankedNodes:
            print("No ranked nodes to generate regex.")
            return []

        regex_parts = []
        for node, score in self.rankedNodes:
            substr = node.label[2]
            if re.match(r'^\d+$', substr):  # Digits
                regex_parts.append(r'\d{3,4}')  # Match groups of 3-4 digits
            elif re.match(r'^[-.()\s]+$', substr):  # Separators
                regex_parts.append(r'[-.()\s]*')  # Match flexible separators
            else:  # Generalize any other substrings
                regex_parts.append(re.escape(substr))

        # Combine fragments into a regex for phone numbers
        if regex_parts:
            combined_regex = ''.join(regex_parts)
            print(f"Generated Regex: {combined_regex}")
            return [combined_regex]

        print("No valid regex generated.")
        return []

    @staticmethod
    def vertDistance(vertex1, vertex2):
        return sum(abs(vertex2[i] - vertex1[i]) for i in vertex1.ids())
    
    def __str__(self):
        # Overloads str function to print a rough text form of the graph.
        # TODO: Make this work.
        pass