"""
Should emit:
B023 - on lines 12, 13, 16, 28, 29, 30, 31, 40, 42, 50, 51, 52, 53, 61, 68.
"""

from functools import reduce

functions = []
z = 0
for x in range(3):
    y = x + 1
    # Subject to late-binding problems
    functions.append(lambda: x)  # B023: 29, "x"
    functions.append(lambda: y)  # not just the loop var  # B023: 29, "y"

    def f_bad_1():
        return x  # B023: 15, "x"

    # Actually OK
    functions.append(lambda x: x * 2)
    functions.append(lambda x=x: x)
    functions.append(lambda: z)  # OK because not assigned in the loop

    def f_ok_1(x):
        return x * 2


def check_inside_functions_too():
    ls = [lambda: x for x in range(2)]  # error  # B023: 18, "x"
    st = {lambda: x for x in range(2)}  # error  # B023: 18, "x"
    gn = (lambda: x for x in range(2))  # error  # B023: 18, "x"
    dt = {x: lambda: x for x in range(2)}  # error  # B023: 21, "x"


async def pointless_async_iterable():
    yield 1


async def container_for_problems():
    async for x in pointless_async_iterable():
        functions.append(lambda: x)  # error  # B023: 33, "x"

    [lambda: x async for x in pointless_async_iterable()]  # error  # B023: 13, "x"


a = 10
b = 0
while True:
    a = a_ = a - 1
    b += 1
    functions.append(lambda: a)  # error  # B023: 29, "a"
    functions.append(lambda: a_)  # error  # B023: 29, "a_"
    functions.append(lambda: b)  # error  # B023: 29, "b"
    functions.append(lambda: c)  # error, but not a name error due to late binding  # B023: 29, "c"
    c: bool = a > 3
    if not c:
        break

# Nested loops should not duplicate reports
for j in range(2):
    for k in range(3):
        lambda: j * k  # error  # B023: 16, "j"  # B023: 20, "k"


for j, k, l in [(1, 2, 3)]:

    def f():
        j = None  # OK because it's an assignment
        [l for k in range(2)]  # error for l, not for k  # B023: 9, "l"

        assert a and functions

    a.attribute = 1  # modifying an attribute doesn't make it a loop variable
    functions[0] = lambda: None  # same for an element

for var in range(2):

    def explicit_capture(captured=var):
        return captured


# `query` is defined in the function, so also defining it in the loop should be OK.
for name in ["a", "b"]:
    query = name

    def myfunc(x):
        query = x
        query_post = x
        _ = query
        _ = query_post

    query_post = name  # in case iteration order matters


# Bug here because two dict comprehensions reference `name`, one of which is inside
# the lambda.  This should be totally fine, of course.
_ = {
    k: v
    for k, v in reduce(
        lambda data, event: merge_mappings(
            [data, {name: f(caches, data, event) for name, f in xx}]
        ),
        events,
        {name: getattr(group, name) for name in yy},
    ).items()
    if k in backfill_fields
}


# OK to define lambdas if they're immediately consumed, typically as the `key=`
# argument or in a consumed `filter()` (even if a comprehension is better style)
for x in range(2):
    # It's not a complete get-out-of-linting-free construct - these should fail:
    min([None, lambda: x], key=repr)  # B023: 23, "x"
    sorted([None, lambda: x], key=repr)  # B023: 26, "x"
    any(filter(bool, [None, lambda: x]))  # B023: 36, "x"
    list(filter(bool, [None, lambda: x]))  # B023: 37, "x"
    all(reduce(bool, [None, lambda: x]))  # B023: 36, "x"

    # But all these ones should be OK:
    min(range(3), key=lambda y: x * y)
    max(range(3), key=lambda y: x * y)
    sorted(range(3), key=lambda y: x * y)

    any(map(lambda y: x < y, range(3)))
    all(map(lambda y: x < y, range(3)))
    set(map(lambda y: x < y, range(3)))
    list(map(lambda y: x < y, range(3)))
    tuple(map(lambda y: x < y, range(3)))
    sorted(map(lambda y: x < y, range(3)))
    frozenset(map(lambda y: x < y, range(3)))

    any(filter(lambda y: x < y, range(3)))
    all(filter(lambda y: x < y, range(3)))
    set(filter(lambda y: x < y, range(3)))
    list(filter(lambda y: x < y, range(3)))
    tuple(filter(lambda y: x < y, range(3)))
    sorted(filter(lambda y: x < y, range(3)))
    frozenset(filter(lambda y: x < y, range(3)))

    any(reduce(lambda y: x | y, range(3)))
    all(reduce(lambda y: x | y, range(3)))
    set(reduce(lambda y: x | y, range(3)))
    list(reduce(lambda y: x | y, range(3)))
    tuple(reduce(lambda y: x | y, range(3)))
    sorted(reduce(lambda y: x | y, range(3)))
    frozenset(reduce(lambda y: x | y, range(3)))

    import functools

    any(functools.reduce(lambda y: x | y, range(3)))
    all(functools.reduce(lambda y: x | y, range(3)))
    set(functools.reduce(lambda y: x | y, range(3)))
    list(functools.reduce(lambda y: x | y, range(3)))
    tuple(functools.reduce(lambda y: x | y, range(3)))
    sorted(functools.reduce(lambda y: x | y, range(3)))
    frozenset(functools.reduce(lambda y: x | y, range(3)))


# OK because the lambda which references a loop variable is defined in a `return`
# statement, and after we return the loop variable can't be redefined.
# In principle we could do something fancy with `break`, but it's not worth it.
def iter_f(names):
    for name in names:
        if exists(name):
            return lambda: name if exists(name) else None

        if foo(name):
            return [lambda: name]  # known false alarm  # B023: 28, "name"

        if False:
            return [lambda: i for i in range(3)]  # error  # B023: 28, "i"