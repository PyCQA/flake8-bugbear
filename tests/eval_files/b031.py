"""
Should emit:
B031 - on lines 30, 34, 43
"""

import itertools
from itertools import groupby

shoppers = ["Jane", "Joe", "Sarah"]
items = [
    ("lettuce", "greens"),
    ("tomatoes", "greens"),
    ("cucumber", "greens"),
    ("chicken breast", "meats & fish"),
    ("salmon", "meats & fish"),
    ("ice cream", "frozen items"),
]

carts = {shopper: [] for shopper in shoppers}


def collect_shop_items(shopper, items):
    # Imagine this an expensive database query or calculation that is
    # advantageous to batch.
    carts[shopper] += items


# Group by shopping section
for _section, section_items in groupby(items, key=lambda p: p[1]):
    for shopper in shoppers:
        collect_shop_items(shopper, section_items) # B031: 36, "section_items"

for _section, section_items in groupby(items, key=lambda p: p[1]):
    collect_shop_items("Jane", section_items)
    collect_shop_items("Joe", section_items) # B031: 30, "section_items"


for _section, section_items in groupby(items, key=lambda p: p[1]):
    # This is ok
    collect_shop_items("Jane", section_items)

for _section, section_items in itertools.groupby(items, key=lambda p: p[1]):
    for shopper in shoppers:
        collect_shop_items(shopper, section_items) # B031: 36, "section_items"

for group in groupby(items, key=lambda p: p[1]):
    # This is bad, but not detected currently
    collect_shop_items("Jane", group[1])
    collect_shop_items("Joe", group[1])


#  Make sure we ignore - but don't fail on more complicated invocations
for _key, (_value1, _value2) in groupby(
    [("a", (1, 2)), ("b", (3, 4)), ("a", (5, 6))], key=lambda p: p[1]
):
    collect_shop_items("Jane", group[1])
    collect_shop_items("Joe", group[1])

#  Make sure we ignore - but don't fail on more complicated invocations
for (_key1, _key2), (_value1, _value2) in groupby(
    [(("a", "a"), (1, 2)), (("b", "b"), (3, 4)), (("a", "a"), (5, 6))],
    key=lambda p: p[1],
):
    collect_shop_items("Jane", group[1])
    collect_shop_items("Joe", group[1])
