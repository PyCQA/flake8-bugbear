"""
Should emit:
B023 - on lines 12, 13, 16, 28, 29, 30, 31, 40, 42, 50, 51, 52, 53.
"""

functions = []
z = 0

for x in range(3):
    y = x + 1
    # Subject to late-binding problems
    functions.append(lambda: x)
    functions.append(lambda: y)  # not just the loop var

    def f_bad_1():
        return x

    # Actually OK
    functions.append(lambda x: x * 2)
    functions.append(lambda x=x: x)
    functions.append(lambda: z)  # OK because not assigned in the loop

    def f_ok_1(x):
        return x * 2


def check_inside_functions_too():
    ls = [lambda: x for x in range(2)]
    st = {lambda: x for x in range(2)}
    gn = (lambda: x for x in range(2))
    dt = {x: lambda: x for x in range(2)}


async def pointless_async_iterable():
    yield 1


async def container_for_problems():
    async for x in pointless_async_iterable():
        functions.append(lambda: x)

    [lambda: x async for x in pointless_async_iterable()]


a = 10
b = 0
while True:
    a = a_ = a - 1
    b += 1
    functions.append(lambda: a)
    functions.append(lambda: a_)
    functions.append(lambda: b)
    functions.append(lambda: c)  # not a name error because of late binding!
    c: bool = a > 3
    if not c:
        break
