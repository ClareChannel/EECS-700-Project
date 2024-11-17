'''
Tokenizer class
Authors: Elizabeth Channel, Samuel Buehler
Description: Class to identify tokens of interest from a body of text using 
             regular expressions.
Date Created: 2024-11-01
Date Modified: 2024-11-16
'''

import re # Imports a library that enables the usage of regular expressions.
          # Documentation for the library can be found here:
          # https://docs.python.org/3/library/re.html

class Tokenizer:
    def __init__(self):
        # Defines the regular expression patterns for different tokens
        self.patterns = {
            #"name": r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b" # Simple full name pattern
            "name": r"\b[A-Z][a-z]*\b", # Potentially better name reg ex.
            # Should allow for an infinitely long name. ('a', 'ab', or 'a' followed by any number of 'b's.)
            # However, it currently only looks for one name, not a multi-part name. Also won't accept hyphenation.
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', # Email pattern
            "phone": r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}\b'  # US phone number
            # Not sure I understand the part of the regex after the or (|).
        }
    
    def tokenize(self, text):
        tokens = []

        for type, pattern in self.patterns.items():
            for match in re.finditer(pattern, text): # Gets all matches of the patterns.
                                                     # https://docs.python.org/3/library/re.html#re.finditer
                tokens.append({
                    "type": type,
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end()
                })
        return sorted(tokens, key=lambda x: x["start"])
        # Returns sorted list of the tokens.
        # https://docs.python.org/3/library/functions.html#sorted
        # key=lambda x is used to sort using the object's index.
        # https://docs.python.org/3/howto/sorting.html#sortinghowto