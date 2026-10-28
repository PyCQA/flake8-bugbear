"""
Should emit:
B911 - on line 13
"""

# A later assignment replaces batched = itertools.batched.
import itertools

import mylib

batched = itertools.batched
batched = mylib.batched
itertools.batched(range(3), 2)  # B911: 0
batched(range(3), 2)
