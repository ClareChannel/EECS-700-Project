'''
Tokenizer class
Authors: Elizabeth Channel, Samuel Buehler
Description: Class to identify tokens of interest from a body of text using 
             regular expressions.
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
            #"name": r"\b[A-Z][a-z]*\b", # Potentially better name reg ex.

            # does not recognize first word in sentence unless it is a name
            #"name": r"(?<!\.\s)(?<!^)([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)", #doesnt work with single name
            #(?<!\.\s): Ensures the match does not follow a period and a space, avoiding picking up the first word of a sentence.
            #(?<!^): Ensures the match does not occur at the very start of the string.
            #[A-Z][a-z]+: Matches a single capitalized word.
            #(?:\s[A-Z][a-z]+)+: Matches one or more additional capitalized words following the first (a typical full name).
            #Grouping with (): Captures the full name as a single match.

            #recognize both full names and single names 
            # while maintaining the constraints of not treating the first capitalized word 
            # in a sentence as a name unless it meets specific conditions
            "name": r"(?<!\.\s)(?<!^)([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)|^(?:(?:[A-Z][a-z]+\s){1}[A-Z][a-z]+)", #not working with first word as name :(
            #(?:\s[A-Z][a-z]+)?: Makes the second word (last name) optional by adding ?
            #(?<!\.\s) and (?<!^): first word of a sentence is not treated as a name

            #none work for hypenation, special characters or titles (eg. Dr., Ms., etc...)

            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', # Email pattern
            "phone": r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}\b|\+\d{11}\b'  # US phone number
            # first : 111-111-1111 format | second : (111) 111-1111 format | third : +12345678900 (international format)
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