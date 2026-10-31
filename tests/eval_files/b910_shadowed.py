"""
Should emit:
B905 - on line 18
"""

# A module-level class named defaultdict is not collections.defaultdict.
import collections


class defaultdict(collections.defaultdict):
    def __missing__(self, key):
        return self.default_factory(key)


_ = defaultdict(int)

# zip() is still the builtin
_ = zip("a", "bc")  # B905: 4
