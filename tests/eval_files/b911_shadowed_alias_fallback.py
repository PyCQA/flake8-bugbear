"""
Should emit:
B911 - on line 18
"""

# A fallback for older Pythons still means batched can be itertools.batched.
import itertools

try:
    batched = itertools.batched
except AttributeError:

    def batched(iterable, n):
        it = iter(iterable)
        return iter(lambda: tuple(itertools.islice(it, n)), ())


batched(range(3), 2)  # B911: 0
