"""
InputDataGraph class
Authors: Elizabeth Channel, Samuel Buehler
Description: Node-Edge-Based class based on BlinkFill and our Project Proposal.
Date Modified: 2024-11-23
"""

import re
from VertexLabel import VertexLabel

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
        prevNode = None
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
            print(f"  {edge}: {patterns}")
        print("--- End of Node and Edge Generation ---\n")


    def __genSubStrExpr(self, input, leftIndex, rightIndex):
        # Generates set of substring expressions.
        pass

#Incorporating positional penalties or rewards based on node adjacency 
# and known phone number structures
    def rankNodes(self):
        """
        Assigns scores to nodes based on their relevance to phone numbers.
        """
        self.rankedNodes = []

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
        print(f"Ranked Nodes: {[str(n[0]) for n in self.rankedNodes]}")



#combining regex patterns directly
    def intersect(self, secondGraph):
        """
        Find the intersection of the graph with another graph.
        """
        newGraph = InputDataGraph("", 0)

        for node1 in self.vertices:
            for node2 in secondGraph.vertices:
                if node1 == node2:
                    newGraph.vertices.add(node1)

        for edge, patterns in self.edges.items():
            if edge in secondGraph.edges:
                newGraph.edges[edge] = self.edges[edge].intersection(secondGraph.edges[edge])

        print(f"Intersected Graph Nodes: {newGraph.vertices}")
        return newGraph

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



    def getDistance(self):
        pass
    
    def __str__(self):
        # Overloads str function to print a rough text form of the graph.
        pass