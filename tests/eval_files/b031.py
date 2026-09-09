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


# Annotating the loop variable is not a second usage of the generator (#465)
for _section, section_items in groupby(items, key=lambda p: p[1]):
    section_items: list
    collect_shop_items("Jane", section_items)


# Mutually exclusive branches cannot consume the group more than once (#465)
for _section, section_items in groupby(items, key=lambda p: p[1]):
    if _section == "greens":
        collect_shop_items("Jane", section_items)
    else:
        collect_shop_items("Joe", section_items)

# Each arm of an if/elif/else chain is also mutually exclusive
for _section, section_items in groupby(items, key=lambda p: p[1]):
    if _section == "greens":
        collect_shop_items("Jane", section_items)
    elif _section == "meats & fish":
        collect_shop_items("Joe", section_items)
    else:
        collect_shop_items("Sarah", section_items)

# Repeated uses on the same path must still warn
for _section, section_items in groupby(items, key=lambda p: p[1]):
    if _section == "greens":
        collect_shop_items("Jane", section_items)
        collect_shop_items("Joe", section_items)  # B031: 34, "section_items"
    else:
        collect_shop_items("Sarah", section_items)

# A use after a conditional can follow a use inside either branch
for _section, section_items in groupby(items, key=lambda p: p[1]):
    if _section == "greens":
        collect_shop_items("Jane", section_items)
    collect_shop_items("Joe", section_items)  # B031: 30, "section_items"

# A use in the condition happens before either branch
for _section, section_items in groupby(items, key=lambda p: p[1]):
    if list(section_items):
        collect_shop_items("Jane", section_items)  # B031: 35, "section_items"
    else:
        collect_shop_items("Joe", section_items)  # B031: 34, "section_items"


# Conditional branches in a repeating while body can run on different iterations
for _section, section_items in groupby(items, key=lambda p: p[1]):
    while shoppers:
        if _section == "greens":
            collect_shop_items("Jane", section_items)  # B031: 39, "section_items"
        else:
            collect_shop_items("Joe", section_items)  # B031: 38, "section_items"


async def async_shoppers():
    yield "Jane"


# The same applies to async for bodies
async def collect_async_groups():
    for _section, section_items in groupby(items, key=lambda p: p[1]):
        async for shopper in async_shoppers():
            if shopper == "Jane":
                collect_shop_items("Jane", section_items)  # B031: 43, "section_items"
            else:
                collect_shop_items("Joe", section_items)  # B031: 42, "section_items"


# Materializing the generator under its original name makes it reusable (#395)
for _section, section_items in groupby(items, key=lambda p: p[1]):
    section_items = list(section_items)
    collect_shop_items("Jane", section_items)
    collect_shop_items("Joe", section_items)

for _section, section_items in groupby(items, key=lambda p: p[1]):
    section_items = tuple(section_items)
    for shopper in shoppers:
        collect_shop_items(shopper, section_items)

# Annotated and chained assignments also replace the original binding
for _, group in groupby(items):
    group: list = list(group)
    print(group)
    print(group)

for _, group in groupby(items):
    saved = group = list(group)
    print(group)
    print(saved)

# The generator is reusable after every branch has materialized it
for _, group in groupby(items):
    if shoppers:
        group = list(group)
    else:
        group = tuple(group)
    print(group)
    print(group)

# A branch that only consumes the generator still makes later uses unsafe
for _, group in groupby(items):
    if shoppers:
        group = list(group)
    else:
        print(group)
    print(group)  # B031: 10, "group"

# A branch can leave the original generator untouched
for _, group in groupby(items):
    if shoppers:
        group = list(group)
    print(group)
    print(group)  # B031: 10, "group"

# Materialization must still warn if the generator has already been used
for _, group in groupby(items):
    print(group)
    group = list(group)  # B031: 17, "group"
    print(group)

# Saving to another name does not make the original generator reusable
for _, group in groupby(items):
    saved = list(group)
    print(group)  # B031: 10, "group"

# Arbitrary calls, including iter(), may return the original iterator
for _, group in groupby(items):
    group = iter(group)
    print(group)  # B031: 10, "group"

# Nested loops may execute zero times, leaving the original generator intact
for _, group in groupby(items):
    for _shopper in shoppers:
        group = list(group)  # B031: 21, "group"
    print(group)
    print(group)  # B031: 10, "group"

for _, group in groupby(items):
    while shoppers:
        group = tuple(group)  # B031: 22, "group"
    print(group)
    print(group)  # B031: 10, "group"

# Assignments in deferred bodies do not replace the enclosing loop variable
for _, group in groupby(items):
    def materialize_later(group):
        if shoppers:
            group = list(group)
        else:
            group = tuple(group)
    print(group)
    print(group)  # B031: 10, "group"
