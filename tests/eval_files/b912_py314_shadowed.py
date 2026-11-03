"""
Should emit:
B905 - on line 18
B913 - on line 18
"""

# A module-level function named map is not the builtin map().
from itertools import zip_longest


def map(function, *iterables):
    return [function(*args) for args in zip_longest(*iterables)]


_ = map(max, "a", "bc")

# zip() is still the builtin
for left, _ in zip("ab", "cd"):  # B913: 10 # B905: 15
    print(left)
