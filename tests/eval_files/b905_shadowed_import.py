"""
Should emit:
B910 - on line 15
"""

# zip() from another library is not the builtin, even after importing that.
from builtins import zip
from collections import defaultdict

from mylib import zip

_ = zip("a", "bc")

# defaultdict() is still collections.defaultdict
_ = defaultdict(int)  # B910: 4
