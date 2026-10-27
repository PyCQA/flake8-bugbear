"""
Should emit:
B911 - on line 11
"""

# Assigning itertools.batched to batched still means itertools.batched.
import itertools

batched = itertools.batched

batched(range(3), 2)  # B911: 0
