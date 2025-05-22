"""
Should emit:
B021 - on lines 14, 22, 30, 38, 46, 54, 62, 70, 73
"""

VARIABLE = "world"


def foo1():
    """hello world!"""


def foo2():
    f"""hello {VARIABLE}!"""  # B021: 4


class bar1:
    """hello world!"""


class bar2:
    f"""hello {VARIABLE}!"""  # B021: 4


def foo1():
    """hello world!"""


def foo2():
    f"""hello {VARIABLE}!"""  # B021: 4


class bar1:
    """hello world!"""


class bar2:
    f"""hello {VARIABLE}!"""  # B021: 4


def foo1():
    "hello world!"


def foo2():
    f"hello {VARIABLE}!"  # B021: 4


class bar1:
    "hello world!"


class bar2:
    f"hello {VARIABLE}!"  # B021: 4


def foo1():
    "hello world!"


def foo2():
    f"hello {VARIABLE}!"  # B021: 4


class bar1:
    "hello world!"


class bar2:
    f"hello {VARIABLE}!"  # B021: 4


def baz():
    f"""I'm probably a docstring: {VARIABLE}!"""  # B021: 4
    print(f"""I'm a normal string""")
    f"""Don't detect me!"""