"""
Should emit:
B018 - on line 21
"""

# A later definition or assignment replaces the imported builtin.
from builtins import filter, map, zip

import mylib


def map(func, items):
    for item in items:
        func(item)


filter = mylib.run_filter
zip = mylib.zip
from builtins import zip

zip([1], [2], strict=True)  # B018: 0, "Call"
map(print, [1, 2])
filter(print, [1, 2])
