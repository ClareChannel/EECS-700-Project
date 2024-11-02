'''
InputDataGraph class
Authors: Elizabeth Channel, Samuel Buehler
Description: Node-Edge-Based class based on BlinkFill and our Project Proposal.
Date Created: 2024-11-01
Date Modified: 2024-11-01
'''

class InputDataGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, token):
        # Based on the add_node from the proposal.
        node = { # Creates a new node
            "type": token["type"],   # Defines the type of a token (alpha, numeral, etc.)
            "value": token["value"], # Defines the value of a token (it's contents/text)
            "start": token["start"], # Position of the first character of the token in the original text
            "end": token["end"]      # Position of the last character of the token in the original text
        }
        self.nodes.append(node) # Add the node to the InputDataGraph
    
    def add_edge(self, prev, next, type):
        # Defines the connections / relationship between nodes.
        # Based on the define_relationships from the proposal.
        edge = {
            "prev": prev,
            "next": next,
            "type": type
        }
        self.edges.append(edge) # Add the edge to the InputDataGraph
    
    # May need a function to connect the nodes by edges in a more efficient way.