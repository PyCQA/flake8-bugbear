"""
Should emit:
B905 - on line 13
"""

# An annotated assignment of builtins.zip to zip still means the builtin, and a
# bare annotation doesn't bind zip at all.
import builtins

zip: object = builtins.zip
zip: object

_ = zip("a", "bc")  # B905: 4
