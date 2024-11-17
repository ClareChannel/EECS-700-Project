'''
Extractor class
Authors: Elizabeth Channel, Samuel Buehler
Description: 
Date Modified: 2024-11-16
'''

class Extractor:
    def __init__(self, graph):
        self.graph = graph

    def extract_info(self):
        extracted_info = {"name": [], "email": [], "phone": []}
        for node in self.graph.nodes:
            if node["type"] in extracted_info:
                extracted_info[node["type"]].append(node["value"])
        return extracted_info