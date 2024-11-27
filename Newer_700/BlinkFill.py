

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

        all_regexes = []
        for graph in self.dataGraphs:
            regexes = graph.getRegExes()
            all_regexes.extend(regexes)

        # Merge regexes into a single pattern
        synthesized_regex = '|'.join(set(all_regexes))
        print(f"Synthesized Regex: {synthesized_regex}")
        return [synthesized_regex]



    
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
    blinkfill.add_example("Call me at (123) 456-7890.", 0)
    regexes = blinkfill.synthesize()
    extractedData = blinkfill.extract("Call me at (123) 456-7890.", regexes)
    print("Extracted Data:", extractedData)







