"""
Intended to store tokens related to the project.
May or may not be necessary, but is good to maintain project scope.
"""

import re

#token definitions include reusable regex patterns 
#for various phone number formats
TOKENS = [
    re.compile("\d+"),
    re.compile("[()\-.\s]+"),
    re.compile("[^\d()\-.\s]+"),
    re.compile("^"),
    re.compile("$")]

def get_token_regex(token_name):
    return TOKENS.get(token_name, None)
