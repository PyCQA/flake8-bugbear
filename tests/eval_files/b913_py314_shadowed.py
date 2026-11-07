"""
Should emit:
B912 - on line 18
"""

# A module-level function named zip is not the builtin zip().
from itertools import zip_longest


def zip(*iterables):
    return zip_longest(*iterables, fillvalue="")


for left, _ in zip("ab", "cd"):
    print(left)

# map() is still the builtin
_ = map(max, "a", "bc")  # B912: 4
