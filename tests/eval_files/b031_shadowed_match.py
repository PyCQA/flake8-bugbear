"""
Should emit:
B031 - on line 28
"""

# A match capture named groupby is not itertools.groupby (#356).
import itertools


def _groupby(x, y):
    return dict().items()


match _groupby:
    case groupby:
        pass

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
