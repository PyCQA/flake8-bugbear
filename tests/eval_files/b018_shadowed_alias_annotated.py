"""
Should emit:
B018 - on line 11
"""

# An annotated assignment of builtins.map to map still means the lazy builtin.
import builtins

map: object = builtins.map

map(print, [1, 2])  # B018: 0, "Call"
