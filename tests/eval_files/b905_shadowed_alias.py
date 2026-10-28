"""
Should emit:
B905 - on line 11
"""

# Assigning builtins.zip to zip still means the builtin.
import builtins

zip = builtins.zip

_ = zip("a", "bc")  # B905: 4
