"""
Should emit:
B020 - on lines 8 and 36
"""

items = [1, 2, 3]

for items in items:  # B020: 4, "items"
    print(items)

items = [1, 2, 3]

for item in items:
    print(item)

values = {"secret": 123}

for key, value in values.items():
    print(f"{key}, {value}")

for key, values in values.items():  # attribute access is safe, not flagged
    print(f"{key}, {values}")

# Variables defined in a comprehension are local in scope
# to that comprehension and are therefore allowed.
for var in [var for var in range(10)]:
    print(var)

for var in (var for var in range(10)):
    print(var)

for k, v in {k: v for k, v in zip(range(10), range(10, 20))}.items():  # B905: 30
    print(k, v)

# However we still call out reassigning the iterable in the comprehension.
for vars in [i for i in vars]:  # B020: 4, "vars"
    print(vars)

for var in sorted(range(10), key=lambda var: var.real):
    print(var)

# Attribute access on loop variable should not trigger B020 (#521)
class Smoother:
    basis = [1, 2]
    smoothers = []

smoother = Smoother()
smoother.smoothers = [Smoother()]

for smoother in smoother.smoothers:
    x = smoother.basis

# Subscript access should not trigger B020
data = {"a": [1, 2]}
for data in data["a"]:
    print(data)
