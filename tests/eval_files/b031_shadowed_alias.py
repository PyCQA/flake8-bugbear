"""
Should emit:
B031 - on line 14
"""

# Assigning itertools.groupby to groupby still means itertools.groupby.
import itertools

groupby = itertools.groupby

for _, v in groupby(None, None):
    if v:
        pass
    if v:  # B031: 7, "v"
        pass
