"""
Should emit:
B911 - on line 11
"""

# When the module doesn't bind batched itself, a function's import of
# itertools.batched still means itertools.batched.
def pairs(iterable):
    from itertools import batched

    return batched(iterable, 2)  # B911: 11
