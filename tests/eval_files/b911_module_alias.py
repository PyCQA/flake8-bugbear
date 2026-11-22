"""
Should emit:
B911 - on lines 10, 17
"""

# batched() from an aliased itertools import is itertools.batched.
import itertools as it

import more_itertools as mit

for chunk in it.batched(range(3), 2):  # B911: 13
    print(chunk)


def chunks(items):
    import itertools as _itertools

    return _itertools.batched(items, 10)  # B911: 11


it.batched(range(3), 2, strict=True)
mit.batched(range(3), 2)
