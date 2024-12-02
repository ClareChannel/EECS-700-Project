"""
Intended to store tokens related to the project.
May or may not be necessary, but is good to maintain project scope.
"""

import re

#token definitions include reusable regex patterns 
#for various phone number formats
TOKENS = {
    "digits": r"\d+",
    "separator": r"[()\-.\s]+",
    "word": r"[^\d()\-.\s]+",
    "startT": r"^",
    "endT": r"$",
}

def get_token_regex(token_name):
    return TOKENS.get(token_name, None)

