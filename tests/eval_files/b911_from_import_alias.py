"""
Should emit:
B911 - on lines 12, 19
"""

# batched() imported from itertools under another name is itertools.batched.
from itertools import batched as bt
from itertools import groupby as batched

from more_itertools import batched as mbt

for chunk in bt(range(3), 2):  # B911: 13
    print(chunk)


def chunks(items):
    from itertools import batched as _batched

    return _batched(items, 10)  # B911: 11


bt(range(3), 2, strict=True)
batched(range(3), 2)
mbt(range(3), 2)
