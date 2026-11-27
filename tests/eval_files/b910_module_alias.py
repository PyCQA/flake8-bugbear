"""
Should emit:
B910 - on lines 11, 17
"""

# defaultdict() from an aliased collections import is collections.defaultdict.
import collections as c

import more_collections as mc

_ = c.defaultdict(int)  # B910: 4


def counts():
    import collections as _collections

    return _collections.defaultdict(int)  # B910: 11


_ = c.defaultdict(list)
_ = mc.defaultdict(int)
