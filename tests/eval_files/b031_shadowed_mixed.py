"""
Should emit:
B031 - on line 13
"""

from itertools import groupby

groupby = groupby

for _, v in groupby(None, None):
    if v:
        pass
    if v:  # B031: 7, "v"
        pass
