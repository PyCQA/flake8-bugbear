"""
Should emit:
B911 - on line 11
"""

import itertools

from mylib import batched

batched(range(3), 2)
itertools.batched(range(3), 2)  # B911: 0
