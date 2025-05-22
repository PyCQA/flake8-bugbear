"""
Should emit:
B013 - on lines 10 and 28
"""

import re

try:
    pass
except (ValueError,):  # B013: 0, "ValueError", ""
    # pointless use of tuple
    pass

# fmt: off
# Turn off black to keep brackets around
# single exception for testing purposes.
try:
    pass
except (ValueError):
    # not using a tuple means it's OK (if odd)
    pass
# fmt: on

try:
    pass
except ValueError:
    # no warning here, all good
    pass

try:
    pass
except (re.error,):  # B013: 0, "re.error", ""
    # pointless use of tuple with dotted attribute
    pass

try:
    pass
except (a.b.c.d, b.c.d):
    # attribute of attribute, etc.
    pass
