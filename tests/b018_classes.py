"""
Should emit:
B018 - on lines 17-26, 30, 33
"""

class Foo1:
    """abc"""


class Foo2:
    """abc"""

    a = 2
    "str"  # Str (no raise)
    f"{int}"  # JoinedStr (no raise)
    1j  # Number (complex)  # B018: 4, "Constant"
    1  # Number (int)  # B018: 4, "Constant"
    1.0  # Number (float)  # B018: 4, "Constant"
    b"foo"  # Binary  # B018: 4, "Constant"
    True  # NameConstant (True)  # B018: 4, "Constant"
    False  # NameConstant (False)  # B018: 4, "Constant"
    None  # NameConstant (None)  # B018: 4, "Constant"
    [1, 2]  # list  # B018: 4, "List"
    {1, 2}  # set  # B018: 4, "Set"
    {"foo": "bar"}  # dict  # B018: 4, "Dict"


class Foo3:
    123  # B018: 4, "Constant"
    a = 2
    "str"
    1  # B018: 4, "Constant"
    (1,)  # bad  # B018: 4, "Tuple"
    (2, 3)  # bad  # B018: 4, "Tuple"
    t = (4, 5)  # good
