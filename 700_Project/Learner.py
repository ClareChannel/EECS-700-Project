'''
Learning Module
Authors: Elizabeth Channel, Samuel Buehler
Description: Class made to train/learn based on predefined examples.
Date Modified: 2024-11-20
'''

import json
import os

class Learner:
    def __init__(self, tokenizer, rules_file="learned_rules.json"):
        self.tokenizer = tokenizer
        self.rules_file = rules_file
        self.learned_patterns = {}  # Patterns refined during training.

        # Load existing rules if available
        self._load_rules()

    def train(self, examples):
        """
        Train the system using example inputs and outputs.

        Args:
            examples (list): A list of dictionaries, each with:
                - `text`: Input text.
                - `output`: Expected structured data (name, email, phone).
        """
        for example in examples:
            text = example['text']
            expected_output = example['output']
            tokens = self.tokenizer.tokenize(text)
            self._learn_from_example(tokens, expected_output)

        # Save learned rules after training
        self._save_rules()

    def _learn_from_example(self, tokens, expected_output):
        """
        Learn patterns or refine rules from a single example.
        """
        for token in tokens:
            token_type = token["type"]
            token_value = token["value"]
            
            if token_type not in self.learned_patterns: # Check if this type of token is in known type of tokens, if not:
                self.learned_patterns[token_type] = [] # Add token type to known token types

            if token_value in expected_output.get(token_type, []): # 
                # Save the token as a valid pattern
                if token_value not in self.learned_patterns[token_type]:
                    print(f"Mismatch: Token '{token['value']}' not in expected {token_type}") # debugging line that displays any token mismatches.
                    self.learned_patterns[token_type].append(token_value)

    def _save_rules(self):
        """
        Save learned patterns to a file.
        """
        with open(self.rules_file, "w") as file:
            json.dump(self.learned_patterns, file, indent=4)

    def _load_rules(self):
        """
        Load learned patterns from a file if it exists.
        """
        if os.path.exists(self.rules_file):
            with open(self.rules_file, "r") as file:
                self.learned_patterns = json.load(file)

    def get_learned_patterns(self):
        """
        Get the currently learned patterns.
        """
        return self.learned_patterns
