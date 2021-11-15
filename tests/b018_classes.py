"""
Should emit:
B018 - on lines 15-26, 30, 32
"""


class Foo1:
    """abc"""


class Foo2:
    """abc"""

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


class Foo3:
    123
    a = 2
    "str"
