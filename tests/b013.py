"""
Should emit:
B013 - on lines 10 and 28
"""

import re

try:
    pass
except (ValueError,):
    # pointless use of tuple
    pass

try:
    pass
except (ValueError):
    # not using a tuple means it's OK (if odd)
    pass

try:
    pass
except ValueError:
    # no warning here, all good
    pass

try:
    pass
except (re.error,):
    # pointless use of tuple with dotted attribute
    pass

try:
    pass
except (a.b.c.d, b.c.d):
    # attribute of attribute, etc.
    pass
