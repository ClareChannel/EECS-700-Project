

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

        all_regexes = set()
        for graph in self.dataGraphs:
            graph.rankNodes()  # Ensure nodes are ranked
            regexes = graph.getRegExes()
            all_regexes.update(regexes)

        # Merge regexes into a single pattern
        synthesized_regex = '|'.join(all_regexes) if all_regexes else ''
        print(f"Synthesized Regex: {synthesized_regex}")
        return [synthesized_regex]



    
    def extract(self, inputString, regexes):
        """
        Apply synthesized regexes to extract phone numbers.
        """
        results = set()
        for regex in regexes:
            print(f"Applying regex: {regex}")  # Debugging applied regex
            try:
                matches = re.findall(regex, inputString)
                print(f"Matches found: {matches}")  # Debugging matches
                results.update(matches)
            except re.error as e:
                print(f"Regex error: {e} with regex {regex}")
        return list(results)



if __name__ == "__main__":
    blinkfill = BlinkFill()

    # Add examples
    examples = [
        "Call me at (123) 456-7890.",
        "Reach me at 987-654-3210.",
        "Contact: 123.456.7890.",
        "Emergency number is 555 123 4567.",
        "Alternate: 2223334444."
    ]
    for i, ex in enumerate(examples):
        blinkfill.add_example(ex, i)

    # Synthesize regex
    regexes = blinkfill.synthesize()

    # Test on new input
    newInput = "My numbers are (555) 123-4578 and 222-333-4444. Also 123.456.7890."
    extractedData = blinkfill.extract(newInput, regexes)
    print(f"Extracted Data: {extractedData}")

