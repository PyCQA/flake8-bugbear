"""
Should emit:
B031 - on line 19
"""

import itertools

from toolz import groupby

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
