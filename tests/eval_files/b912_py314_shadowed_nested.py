"""
Should emit:
B912 - on line 22
"""

# Only module-level bindings replace map. A method or class attribute of that
# name, or an import that only runs on Python 2, leaves the module's map() the
# builtin.
import sys

if sys.version_info < (3,):
    from itertools import imap as map


class Pool:
    map = None

    def map(self, function, *iterables):
        return self


_ = map(max, "a", "bc")  # B912: 4
