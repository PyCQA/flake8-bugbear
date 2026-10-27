"""
Should emit:
B018 - on line 11
"""

# Assigning builtins.map to map still means the lazy builtin.
import builtins

map = builtins.map

map(print, [1, 2])  # B018: 0, "Call"
