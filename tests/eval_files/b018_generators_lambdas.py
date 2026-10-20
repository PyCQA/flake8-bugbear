"""
Should emit:
B018 - on lines 11-17
"""


def discarded(items, log, debug_func):
    # a generator expression is lazy: as a statement, its body never runs (#452)
    # and a lambda that isn't assigned or passed anywhere can never be called
    log("start")
    (print(item) for item in items)  # B018: 4, "GeneratorExp"
    (item.close() for item in items if item)  # B018: 4, "GeneratorExp"
    (x for x in items)  # B018: 4, "GeneratorExp"
    lambda: log("done")  # B018: 4, "Lambda"
    lambda item, /, *rest, key=None, **kwargs: item  # B018: 4, "Lambda"
    if not debug_func:
        lambda x: True  # B018: 8, "Lambda"
    return debug_func


def used(items, log):
    consume = list(print(item) for item in items)
    log(lambda: "done")
    total = sum(x for x in items)
    callback = lambda: log("done")  # noqa: E731
    [print(item) for item in items]
    return consume, total, callback


def expected_to_raise(raises):
    # directly in a `try` or `with` block, a generator expression may be built
    # only to see `iter()` raise on its first iterable
    with raises(TypeError):
        (x for x in 1)
    try:
        (x for x in None)
    except TypeError:
        pass
