"""
Should emit:
B018 - on lines 11-24
"""

something()
assert issubclass(object, int)
x = sorted(foo)

# calls to be found
all()  # B018: 0, "Call"
any()  # B018: 0, "Call"
dict()  # B018: 0, "Call"
frozenset()  # B018: 0, "Call"
isinstance()  # B018: 0, "Call"
issubclass()  # B018: 0, "Call"
len()  # B018: 0, "Call"
max()  # B018: 0, "Call"
min()  # B018: 0, "Call"
repr()  # B018: 0, "Call"
set()  # B018: 0, "Call"
sorted()  # B018: 0, "Call"
str()  # B018: 0, "Call"
tuple()  # B018: 0, "Call"
