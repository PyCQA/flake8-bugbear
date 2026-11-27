"""
Should emit:
B031 - on line 17
"""

# groupby() imported from itertools under another name is itertools.groupby.
from itertools import groupby as gb

from other import groupby as ogb

for _, group in ogb(None, None):
    list(group)
    list(group)

for _, group in gb(None, None):
    list(group)
    list(group)  # B031: 9, "group"
