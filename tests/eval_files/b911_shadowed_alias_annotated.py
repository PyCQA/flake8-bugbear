"""
Should emit:
B911 - on line 12
"""

# An annotated assignment of itertools.batched to batched still means
# itertools.batched.
import itertools

batched: object = itertools.batched

batched(range(3), 2)  # B911: 0
