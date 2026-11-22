"""
Should emit:
B031 - on line 16
"""

# groupby() from an aliased itertools import is itertools.groupby.
import itertools as it

import other as ot

for _, group in ot.groupby(None, None):
    list(group)
    list(group)

for _, group in it.groupby(None, None):
    list(group)
    list(group)  # B031: 9, "group"
