"""
Should emit:
B031 - on line 24
"""

# A module-level function named groupby is not itertools.groupby (#356).
import itertools


def groupby(x, y):
    return dict().items()


for _, v in groupby(None, None):
    if v:
        pass
    if v:
        pass


for _, v in itertools.groupby(None, None):
    if v:
        pass
    if v:  # B031: 7, "v"
        pass
