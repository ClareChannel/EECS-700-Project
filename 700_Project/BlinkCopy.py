'''
Main
Authors: Elizabeth Channel, Samuel Buehler
Description: 
Date Modified: 2024-11-16
'''

import json
from InputDataGraph import InputDataGraph
from Tokenizer import Tokenizer
from Extractor import Extractor
from Learner import Learner

class BlinkCopy:
    def __init__(self, rules_file="learned_rules.json"):
        self.tokenizer = Tokenizer()
        self.graph = InputDataGraph()
        self.extractor = Extractor(self.graph)
        self.learner = Learner(self.tokenizer, rules_file)

    def train_from_file(self, examples_file):
        """
        Train the BlinkCopy system using examples from a JSON file.

        Args:
            examples_file (str): Path to the JSON file containing training examples.
        """
        with open(examples_file, "r") as file:
            examples = json.load(file)
        self.learner.train(examples)

    def process_text(self, text: str):
        """
        Process input text to extract information.
        """
        # Tokenize using learned patterns if available
        tokens = self.tokenizer.tokenize(text)

        # Add tokens to the graph.
        for token in tokens:
            self.graph.add_node(token)

        # Establish relationships.
        for i in range(len(tokens) - 1):
            self.graph.add_edge(tokens[i], tokens[i + 1], "sequential")

        # Extract structured information.
        return self.extractor.extract_info()

if __name__ == "__main__":
    blink_copy = BlinkCopy()

    # Train the model using examples from a JSON file
    training_file = "examples.json"
    blink_copy.train_from_file(training_file)

    # Test with new input
    test_text = "Hello, I am Mark Spencer, my phone number is 555-123-4567, you can email me at mark.spencer@company.com."
    extracted_data = blink_copy.process_text(test_text)

    print("Extracted Data:", extracted_data)


