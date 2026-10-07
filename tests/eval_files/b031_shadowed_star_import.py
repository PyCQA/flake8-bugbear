"""
Should emit:
B031 - on line 13
"""

# A star import from itertools still counts as itertools.groupby (#356).
groupby = None
from itertools import *

for _, v in groupby(None, None):
    if v:
        pass
    if v:  # B031: 7, "v"
        pass
