"""
Should emit:
B905 - on line 13
"""

# defaultdict() from another library is not collections.defaultdict.
from mylib import defaultdict

_ = defaultdict(int)
_ = defaultdict(int, {"a": 1})

# zip() is still the builtin
_ = zip("a", "bc")  # B905: 4
