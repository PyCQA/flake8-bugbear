"""
Should emit:
B020 - on lines 8 and 21
"""

items = [1, 2, 3]

for items in items:
    print(items)

items = [1, 2, 3]

for item in items:
    print(item)

values = {"secret": 123}

for key, value in values.items():
    print(f"{key}, {value}")

for key, values in values.items():
    print(f"{key}, {values}")
