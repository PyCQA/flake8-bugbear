"""
Should emit:
B018 - on lines 11-19 and 58
"""


def discarded(items, log, debug_func):
    # a generator expression is lazy: as a statement, its body never runs (#452)
    # and a lambda that isn't assigned or passed anywhere can never be called
    log("start")
    (print(item) for item in items)  # B018: 4, "GeneratorExp"
    (item.close() for item in items if item)  # B018: 4, "GeneratorExp"
    (x for x in items)  # B018: 4, "GeneratorExp"
    (y for x in items for y in log(x))  # B018: 4, "GeneratorExp"
    lambda: log("done")  # B018: 4, "Lambda"
    lambda item, /, *rest, key=None, **kwargs: item  # B018: 4, "Lambda"
    lambda item=-1, *, key=len: item  # B018: 4, "Lambda"
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


def evaluated_right_away(record, refresh):
    # the first iterable of a generator expression and the defaults of a lambda
    # are evaluated right away, so a call in them still runs
    (x for x in refresh())
    lambda arg=record(): None
    lambda *, arg=record(): None


async def awaited_right_away(refresh, pending):
    (x for x in await refresh())
    lambda arg=await pending: arg


def expected_to_raise(raises):
    # directly in a `try` or `with` block, a generator expression or a lambda
    # with defaults may be built only to see its first iterable or a default raise
    with raises(TypeError):
        (x for x in 1)
    try:
        (x for x in None)
    except TypeError:
        pass
    with raises(ZeroDivisionError):
        lambda arg=1 / 0: arg
    # a lambda without defaults evaluates nothing, so it can't raise
    with raises(ZeroDivisionError):
        lambda: 1 / 0  # B018: 8, "Lambda"
