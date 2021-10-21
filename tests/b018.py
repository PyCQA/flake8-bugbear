"""
Should emit:
B018 - on lines 14, 19, 30, 35
"""


def foo1():
    """my docstring"""


def foo2():
    """my docstring"""
    a = 2
    "str"


def foo3():
    a = 2
    "str"


class Foo1:
    """abc"""


class Foo2:
    """abc"""

    a = 2
    "str"


class Foo3:
    a = 2
    "str"
