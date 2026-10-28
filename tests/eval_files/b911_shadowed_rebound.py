"""
Should emit:
B911 - on line 17
"""

# A later definition replaces the imported itertools.batched.
import itertools
from itertools import batched


def batched(iterable, n):
    it = iter(iterable)
    return iter(lambda: tuple(itertools.islice(it, n)), ())


batched(range(3), 2)
itertools.batched(range(3), 2)  # B911: 0
