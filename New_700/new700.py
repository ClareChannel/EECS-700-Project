import re
import json
from typing import List, Tuple
import InputDataGraph

class RegexSynthesizer:
    def __init__(self, rules_file: str = "learned_rules.json"):
        """
        Initialize the synthesizer with a file to store/load rules.
        Args:
            rules_file: Path to the file storing learned regex rules.
        """
        self.rules_file = rules_file
        self.learned_patterns = self._load_rules()
    
    def _load_rules(self) -> List[str]:
        """Load learned rules from the rules file."""
        try:
            with open(self.rules_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_rules(self):
        """Save the current learned rules to the rules file."""
        with open(self.rules_file, "w") as f:
            json.dump(self.learned_patterns, f, indent=4)

    def learn_from_examples(self, examples: List[Tuple[str, str]]):
        """
        Learn regex patterns from examples and update the learned patterns.
        Args:
            examples: A list of tuples (input_text, expected_phone_number).
        """
        for input_text, expected_output in examples:
            # Escape and generalize the expected output
            escaped_output = re.escape(expected_output)
            generalized_output = re.sub(r'\d', r'\\d', escaped_output)
            pattern = generalized_output.replace(r'\d', r'\d+').replace(r'\.', r'\W')
            if pattern not in self.learned_patterns:
                self.learned_patterns.append(pattern)
        self._save_rules()

    def extract(self, text: str) -> List[str]:
        """
        Extract phone numbers from text using the learned regex.
        Args:
            text: The text to search for phone numbers.
        Returns:
            A list of matched phone numbers.
        """
        if not self.learned_patterns:
            raise ValueError("No regex learned yet. Provide examples first.")
        # Combine all patterns into one regex
        combined_regex = "|".join(f"({pattern})" for pattern in self.learned_patterns)
        matches = re.findall(combined_regex, text)
        # Flatten the results to get only non-empty groups
        return [match[0] for match in matches if match[0]]

    @staticmethod
    def load_examples_from_file(file_path: str) -> List[Tuple[str, str]]:
        """
        Load examples from a file.
        Args:
            file_path: Path to the file containing examples.
        Returns:
            A list of tuples (input_text, expected_phone_number).
        """
        examples = []
        with open(file_path, "r") as f:
            for line in f:
                parts = line.strip().split(",", 1)  # Split into input_text and expected_output
                if len(parts) == 2:
                    examples.append((parts[0], parts[1]))
        return examples

# Example usage
if __name__ == "__main__":
    # Initialize synthesizer with a rules file
    synthesizer = RegexSynthesizer()

    # Load examples from a file
    examples_file = "examples.txt"  # File should have lines like: "text,phone_number"
    examples = synthesizer.load_examples_from_file(examples_file)
    
    # Learn from examples
    synthesizer.learn_from_examples(examples)
    print("Learned Patterns:", synthesizer.learned_patterns)

    # Test the regex on new text
    test_text = "Contact us at (123) 456-7890 or 321-654-0987."
    extracted_numbers = synthesizer.extract(test_text)
    print("Extracted Phone Numbers:", extracted_numbers)
