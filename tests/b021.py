"""
Should emit:
B021 - on lines 14, 22
"""

VARIABLE = "world"


def foo1():
    """hello world!"""


def foo2():
    f"""hello {VARIABLE}!"""


class bar1:
    """hello world!"""


class bar2:
    f"""hello {VARIABLE}!"""
