"""
Should emit:
B018 - on lines 14-25, 29, 31
"""


def foo1():
    """my docstring"""


def foo2():
    """my docstring"""
    a = 2
    "str"  # Str
    1j  # Number (complex)
    1  # Number (int)
    1.0  # Number (float)
    b"foo"  # Binary
    f"{int}"  # JoinedStr
    True  # NameConstant (True)
    False  # NameConstant (False)
    None  # NameConstant (None)
    [1, 2]  # list
    {1, 2}  # set
    {"foo": "bar"}  # dict


def foo3():
    123
    a = 2
    "str"
