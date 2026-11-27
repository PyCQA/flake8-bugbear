import collections
from collections import defaultdict

a = defaultdict(int) # B910: 4
b = defaultdict(float)
c = defaultdict(bool)
d = defaultdict(str)
e = defaultdict()
f = defaultdict(int) # B910: 4

# The same call, spelled with the module: `collections.defaultdict(int)`.
g = collections.defaultdict(int)  # B910: 4
h = collections.defaultdict(float)
i = collections.defaultdict()
j = collections.defaultdict(int, {"a": 1})  # B910: 4
