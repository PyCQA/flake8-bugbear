"""
Should emit:
B905 - on lines 14, 15, 16
"""

# count(), cycle() and repeat() that aren't from itertools may be finite.
from mylib import repeat


def count():
    return range(3)


_ = zip([1, 2, 3], count())  # B905: 4
_ = zip([1, 2, 3], repeat(1))  # B905: 4
_ = zip([1, 2, 3], cycle("ABCDEF"))  # B905: 4
