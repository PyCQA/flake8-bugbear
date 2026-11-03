"""
Should emit:
B905 - on line 23
B913 - on line 23
"""

# Only module-level bindings replace zip. A method or class attribute of that
# name, or an import that only runs on Python 2, leaves the module's zip() the
# builtin.
import sys

if sys.version_info < (3,):
    from itertools import izip as zip


class Archive:
    zip = None

    def zip(self, other):
        return self


for left, _ in zip("ab", "cd"):  # B913: 10 # B905: 15
    print(left)
