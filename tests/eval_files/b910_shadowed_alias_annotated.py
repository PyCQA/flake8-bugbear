"""
Should emit:
B910 - on line 13
"""

# An annotated assignment of collections.defaultdict to defaultdict still means
# collections.defaultdict, and a bare annotation doesn't bind it at all.
import collections

defaultdict: type = collections.defaultdict
defaultdict: type

_ = defaultdict(int)  # B910: 4
