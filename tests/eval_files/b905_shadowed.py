"""
Should emit:
B910 - on line 18
"""

# A module-level function named zip is not the builtin zip().
from collections import defaultdict
from itertools import zip_longest


def zip(*iterables):
    return zip_longest(*iterables, fillvalue="")


_ = zip("a", "bc")

# defaultdict() is still collections.defaultdict
_ = defaultdict(int)  # B910: 4
