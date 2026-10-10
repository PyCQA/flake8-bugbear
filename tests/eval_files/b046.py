import collections
from collections import OrderedDict

keys = ("a", "b")

# bad
dict.fromkeys(keys, [])  # B046: 20
dict.fromkeys(keys, {})  # B046: 20
dict.fromkeys(keys, {1, 2})  # B046: 20
dict.fromkeys(keys, [x for x in range(3)])  # B046: 20
dict.fromkeys(keys, {x: x for x in range(3)})  # B046: 20
dict.fromkeys(keys, {x for x in range(3)})  # B046: 20
dict.fromkeys(keys, list())  # B046: 20
dict.fromkeys(keys, dict())  # B046: 20
dict.fromkeys(keys, set())  # B046: 20
dict.fromkeys(keys, collections.defaultdict(list))  # B046: 20
dict.fromkeys(keys, collections.Counter())  # B046: 20
OrderedDict.fromkeys(keys, [])  # B046: 27
collections.OrderedDict.fromkeys(keys, [])  # B046: 39
OrderedDict.fromkeys(keys, value=[])  # B046: 33
dict.fromkeys(["a", "b"], [])  # B046: 26

# good
dict.fromkeys(keys)
dict.fromkeys(keys, None)
dict.fromkeys(keys, 0)
dict.fromkeys(keys, "")
dict.fromkeys(keys, ())
dict.fromkeys(keys, tuple())
dict.fromkeys(keys, frozenset())
dict.fromkeys(keys, value)
dict.fromkeys(keys, make_default())
OrderedDict.fromkeys(keys, value=None)
{key: [] for key in keys}
other.fromkeys(keys, [])
