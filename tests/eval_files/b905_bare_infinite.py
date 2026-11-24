"""
Should emit:
B905 - on lines 20, 21
"""

# count(), cycle() and repeat() imported from itertools are infinite.
from itertools import count, cycle

_ = zip([1, 2, 3], cycle("ABCDEF"))
_ = zip([1, 2, 3], count())


def pairs(items):
    from itertools import repeat

    _ = zip(items, repeat(1))
    _ = zip(items, repeat(1, None))
    _ = zip(items, repeat(1, times=None))

    _ = zip(items, repeat(1, 1))  # B905: 8
    _ = zip(items, map(str, count()))  # B905: 8
