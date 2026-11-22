"""
Should emit:
B905 - on lines 13, 14, 15
"""

# Infinite iterators from an aliased itertools import don't need strict=.
import itertools as it

_ = zip([1, 2, 3], it.cycle("ABCDEF"))
_ = zip([1, 2, 3], it.count())
_ = zip([1, 2, 3], it.repeat(1))

_ = zip([1, 2, 3], it.repeat(1, 1))  # B905: 4
_ = zip([1, 2, 3], it.islice("ABCDEF", 3))  # B905: 4
_ = zip([1, 2, 3], other.cycle("ABCDEF"))  # B905: 4
