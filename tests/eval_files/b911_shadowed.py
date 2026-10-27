"""
Should emit:
B911 - on line 16
"""

# A module-level function named batched is not itertools.batched.
import itertools


def batched(iterable, n):
    it = iter(iterable)
    return iter(lambda: tuple(itertools.islice(it, n)), ())


batched(range(3), 2)
itertools.batched(range(3), 2)  # B911: 0
