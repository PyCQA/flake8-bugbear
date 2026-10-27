"""
Should emit:
B018 - on lines 13-14
"""

from builtins import filter

# map() and reversed() from another library are not the lazy builtins.
from mylib import map, reversed

map(print, [1, 2])
reversed([1, 2])
filter(None, [1, 2])  # B018: 0, "Call"
enumerate([1, 2])  # B018: 0, "Call"
