import re
from InputDataGraph import InputDataGraph

class BlinkFill:
    """
    BlinkFill implementation for extracting phone numbers using InputDataGraph.
    """

    def __init__(self):
        #self.dataGraphs = []
        self.IDG = None

    def add_example(self, inputString, index):
        """
        Creates a child IDG using the given example and intersects it with the parent IDG.
        """
        dataGraph = InputDataGraph(inputString, index)
        #self.dataGraphs.append(dataGraph) # TODO: Replace with intersection of new child IDG and parent IDG.
        if self.IDG is None: # If this is the first IDG created,
            self.IDG = dataGraph # Set this IDG as the parent IDG
        else: # If this is not the first IDG created,
            self.IDG.intersect(dataGraph) # Intersect the child IDG with the parent IDG.
    
    def synthesize(self):
        """
        Combine patterns across all data graphs to synthesize a single regex.
        NOTE: I think this needs to be redone entirely once the IDG intersection is working.
              I believe, ideally, that this function should try many or all of the paths
              through the parent IDG, and compare the generated output to the given output.
              When there's an output match, that's the regex it returns.
              Considering this, we may need to teach the program (in the IDG file) how to
              mark certain parts of a regex as "optional". That or we just have it OR (|)
              together all regexes that led to successful output matches. That may be easier.
        """
        if self.IDG is None:
            raise ValueError("No examples provided.")

        all_regexes = set()
        #for graph in self.dataGraphs:
        self.IDG.rankNodes()  # Ensure nodes are ranked
        regexes = self.IDG.getRegExes()
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
    examples = [ "Call me at (123) 456-7890." ]
    #examples = [ ("Call me at (123) 456-7890.", "(123) 456-7890") ]
    '''examples = [
        "Call me at (123) 456-7890.",
        "Reach me at 987-654-3210.",
        "Contact: 123.456.7890.",
        "Emergency number is 555 123 4567.",
        "Alternate: 2223334444."
    ]'''
    for i, ex in enumerate(examples):
        blinkfill.add_example(ex, i)

    # Synthesize regex
    regexes = blinkfill.synthesize()

    # Test on new input
    ''' # Temporarily commenting this out.
        # We should focus on getting it to work correctly with the input/output examples first.

    newInput = "My numbers are (555) 123-4578 and 222-333-4444. Also 123.456.7890."
    extractedData = blinkfill.extract(newInput, regexes)
    print(f"Extracted Data: {extractedData}")
    '''