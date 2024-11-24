"""
Intended to store tokens related to the project.
May or may not be necessary, but is good to maintain project scope.
"""

import re

# Based on the original BlinkFill paper.
#  Token        Regex       Abbr.
#  digits       '\d+'       d
#  startT       '^'         ^
#  endT         '$'         $