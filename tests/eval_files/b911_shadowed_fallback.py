"""
Should emit:
B911 - on line 17
"""

# A fallback for older Pythons still means batched can be itertools.batched.
try:
    from itertools import batched
except ImportError:
    import itertools

    def batched(iterable, n):
        it = iter(iterable)
        return iter(lambda: tuple(itertools.islice(it, n)), ())


batched(range(3), 2)  # B911: 0
