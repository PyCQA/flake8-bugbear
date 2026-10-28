"""
Should emit:
B910 - on line 11
"""

# Assigning collections.defaultdict to defaultdict still means collections.
import collections

defaultdict = collections.defaultdict

_ = defaultdict(int)  # B910: 4
