"""
Should emit:
B910 - on line 28
"""

# A function's local zip = builtins.zip, or a class attribute, doesn't make the
# module's own zip() the builtin.
import builtins
from collections import defaultdict


def zip(*args):
    return list(builtins.zip(*args))


def pairs(a, b):
    zip = builtins.zip
    return zip(a, b, strict=True)


class Pairs:
    zip = builtins.zip


_ = zip("a", "bc")

# defaultdict() is still collections.defaultdict
_ = defaultdict(int)  # B910: 4
