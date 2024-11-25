

import re
from InputDataGraph import InputDataGraph

class BlinkFill:
    """
    BlinkFill implementation for extracting phone numbers using InputDataGraph.
    """

    def __init__(self):
        self.dataGraphs = []

    def add_example(self, inputString, index):
        """
        """
        dataGraph = InputDataGraph(inputString, index)
        self.dataGraphs.append(dataGraph)
    
    def synthesize(self):
        """
        """
        if not self.dataGraphs:
            raise ValueError("No examples provided.")
        
        # Intersect all data graphs to find common patterns
        intersectedGraph = self.dataGraphs[0]
        for graph in self.dataGraphs[1:]:
            intersectedGraph = intersectedGraph.intersect(graph)
        
        # Rank nodes and generated regular expressions
        intersectedGraph.rankNodes()
        return intersectedGraph.getRegExes()
    
    def extract(self, inputString, regexes):
        """
        """
        results = set()
        for regex in regexes:
            matches = re.findall(regex, inputString)
            results.update(matches)
        return list(results)

if __name__ == "__main__":
    blinkfill = BlinkFill()

    blinkfill.add_example("Call me at (123) 456-7890.", 0)
    blinkfill.add_example("Reach me at 987-654-3210.", 1)

    regexes = blinkfill.synthesize()
    print("Synthesized Regexes:", regexes)

    newInput = "My numbers are (555) 123-4578 and 222-333-4444."
    extractedData = blinkfill.extract(newInput, regexes)
    print("Extracted Data:", extractedData)