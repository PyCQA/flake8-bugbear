"""
Should emit:
B031 - on line 15
"""

# An annotated assignment of itertools.groupby to groupby still means
# itertools.groupby.
import itertools

groupby: object = itertools.groupby

for _, v in groupby(None, None):
    if v:
        pass
    if v:  # B031: 7, "v"
        pass
