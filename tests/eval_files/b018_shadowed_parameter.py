"""
Should emit:
B018 - on line 19
"""

# A parameter named map or filter is not the lazy builtin: it may be an
# executor's map() passed in, which does run the function.


def run_all(func, items, map):
    map(func, items)


def run_matching(func, items, *, filter):
    filter(func, items)


def check(items):
    enumerate(items)  # B018: 4, "Call"
