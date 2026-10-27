"""
Should emit:
B018 - on line 21
"""

# The module's own map() and filter() are not the lazy builtins, so calling
# them as a statement may well do the work.
import concurrent.futures


def map(func, items):
    for item in items:
        func(item)


filter = concurrent.futures.ThreadPoolExecutor().map

map(print, [1, 2])
filter(print, [1, 2])
# zip() is still the builtin
zip([1], [2], strict=True)  # B018: 0, "Call"
