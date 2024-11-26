

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
        Combine patterns across all data graphs to synthesize a single regex.
        """
        if not self.dataGraphs:
            raise ValueError("No examples provided.")
        
        # Start with the first data graph
        intersectedGraph = self.dataGraphs[0]
        
        # Intersect with subsequent graphs
        for graph in self.dataGraphs[1:]:
            intersectedGraph = intersectedGraph.intersect(graph)
        
        # Rank nodes and extract regexes
        intersectedGraph.rankNodes()
        regexes = intersectedGraph.getRegExes()

        # Debugging synthesized regex
        print(f"Synthesized Regexes: {regexes}")
        return regexes


    
    def extract(self, inputString, regexes):
        """
        Apply synthesized regexes to extract phone numbers.
        """
        results = set()
        for regex in regexes:
            print(f"Applying regex: {regex}")  # Debugging applied regex
            matches = re.findall(regex, inputString)
            print(f"Matches found: {matches}")  # Debugging matches
            results.update(matches)
        return list(results)




if __name__ == "__main__":
    blinkfill = BlinkFill()

    # Add more examples
    blinkfill.add_example("Call me at (123) 456-7890.", 0)
    blinkfill.add_example("Reach me at 987-654-3210.", 1)
    blinkfill.add_example("Contact: 123.456.7890.", 2)
    blinkfill.add_example("Emergency number is 555 123 4567.", 3)
    blinkfill.add_example("Alternate: 2223334444.", 4)

    # Synthesize regex
    regexes = blinkfill.synthesize()

    # Test on new input
    newInput = "My numbers are (555) 123-4578 and 222-333-4444. Also 123.456.7890."
    extractedData = blinkfill.extract(newInput, regexes)
    print("Extracted Data:", extractedData)




