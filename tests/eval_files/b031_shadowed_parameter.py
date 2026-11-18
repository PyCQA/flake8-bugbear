"""
Should emit:
B031 - on line 21
"""

# A parameter named groupby is not itertools.groupby.
import itertools


def summarize(rows, key, groupby):
    for _, group in groupby(rows, key):
        if group:
            pass
        if group:
            pass


for _, v in itertools.groupby(None, None):
    if v:
        pass
    if v:  # B031: 7, "v"
        pass
