'''
Main
Authors: Elizabeth Channel, Samuel Buehler
Description: 
Date Created: 2024-11-16
Date Modified: 2024-11-16
'''

from InputDataGraph import InputDataGraph
from Tokenizer import Tokenizer
from Extractor import Extractor

class BlinkCopy:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.graph = InputDataGraph()
        self.extractor = Extractor(self.graph)

    def process_text(self, text: str):
        # Step 1: Tokenize the text.
        tokens = self.tokenizer.tokenize(text)
        
        # Step 2: Add tokens to the graph.
        for token in tokens:
            self.graph.add_node(token)
        
        # Step 3: Establish relationships (sequential edges in this example).
        for i in range(len(tokens) - 1):
            self.graph.add_edge(tokens[i], tokens[i + 1], "sequential")
        
        # Step 4: Extract and return structured information.
        return self.extractor.extract_info()

# Example Usage
if __name__ == "__main__":
    blink_copy = BlinkCopy()
    sample_text = "John Doe, contact me at john.doe@example.com or (123) 456-7890."
    extracted_data = blink_copy.process_text(sample_text)
    print(extracted_data)
