"""
Should emit:
B905 - on line 25
B910 - on line 26
"""

# Only module-level bindings replace zip and defaultdict. A method or class
# attribute of that name, or an import that only runs on Python 2, leaves the
# module's zip() the builtin.
import sys
from collections import defaultdict

if sys.version_info < (3,):
    from itertools import izip as zip


class Archive:
    zip = None
    defaultdict = None

    def zip(self, other):
        return self


_ = zip("a", "bc")  # B905: 4
_ = defaultdict(int)  # B910: 4
