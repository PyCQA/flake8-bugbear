"""
Should emit:
B911 - on line 27
"""

# A function's own import of itertools.batched, or a class attribute, is local
# to it, so the module's batched() stays the module's own function.
import itertools


def batched(iterable, n):
    it = iter(iterable)
    return iter(lambda: tuple(itertools.islice(it, n)), ())


def pairs(iterable):
    from itertools import batched

    return batched(iterable, 2, strict=True)


class Pairs:
    batched = itertools.batched


batched(range(3), 2)
itertools.batched(range(3), 2)  # B911: 0
