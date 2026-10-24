"""
Should emit:
B018 - on lines 11-18 and 21
"""


def discarded(items, names, values, handle, fetch):
    # map(), filter(), reversed(), zip() and enumerate() return lazy iterators:
    # as a statement, nothing ever iterates over them, so the function they get
    # is never called (#452)
    map(print, items)  # B018: 4, "Call"
    map(lambda item: item.save(), items)  # B018: 4, "Call"
    filter(handle, items)  # B018: 4, "Call"
    reversed(items)  # B018: 4, "Call"
    zip(names, values, strict=True)  # B018: 4, "Call"
    enumerate(items)  # B018: 4, "Call"
    # `fetch` is still called here, but `handle` never is
    map(handle, fetch())  # B018: 4, "Call"
    for item in items:
        if item:
            map(handle, item)  # B018: 12, "Call"


def used(items, names, values, handle, pool):
    list(map(print, items))
    handled = map(handle, items)
    for name, value in zip(names, values, strict=True):
        handle(name, value)
    pool.map(handle, items)
    items.reverse()
    # iter() calls `__iter__` right away
    iter(items)
    next(iter(items))
    return handled, filter(handle, items), [reversed(items), enumerate(items)]


def expected_to_raise(raises, obj):
    # directly in a `try` or `with` block, a lazy builtin may be called only to
    # see it raise, since it checks its arguments right away
    with raises(TypeError):
        zip(1, strict=True)
    with raises(TypeError):
        map(print, obj)
    try:
        reversed(obj)
    except TypeError:
        pass
