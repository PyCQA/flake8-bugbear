"""
Should emit:
B901
"""

def broken():
    if True:
        return [1, 2, 3]  # B901

    yield 3
    yield 2
    yield 1


def not_broken():
    if True:
        return

    yield 3
    yield 2
    yield 1


def not_broken2():
    return not_broken()


def not_broken3():
    return

    yield from not_broken()


def broken2():
    return [3, 2, 1]  # B901

    yield from not_broken()


async def not_broken4():
    import asyncio

    await asyncio.sleep(1)
    return 1


def not_broken5():
    def inner():
        return 2

    yield inner()


def not_broken6():
    return (yield from [])


def not_broken7():
    x = yield from []
    return x


def not_broken8():
    x = None

    def inner(ex):
        nonlocal x
        x = ex

    inner((yield from []))
    return x


class NotBroken9(object):
    def __await__(self):
        yield from function()
        return 42


def broken3():
    if True:
        return [1, 2, 3]  # B901
    else:
        yield 3


def broken4() -> Iterable[str]:
    yield "x"
    return ["x"]  # B901


def broken5() -> Generator[str]:
    yield "x"
    return ["x"]  # B901


def not_broken10() -> Generator[str, int, float]:
    yield "x"
    return 1.0


def not_broken11() -> typing.Generator[str, int, float]:
    yield "x"
    return 1.0


def not_broken12() -> collections.abc.Generator[str, int, float]:
    yield "x"
    return 1.0
