"""
Should emit:
B905 - on line 24
"""

# A function's local defaultdict = collections.defaultdict doesn't make the
# module's own defaultdict class collections.defaultdict.
import collections


class defaultdict(collections.defaultdict):
    def __missing__(self, key):
        return self.default_factory(key)


def counts():
    defaultdict = collections.defaultdict
    return defaultdict(list)


_ = defaultdict(int)

# zip() is still the builtin
_ = zip("a", "bc")  # B905: 4
