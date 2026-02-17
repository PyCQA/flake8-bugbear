"""
Should emit:
B018 - on lines 16-25, 29, 32, 42-50
"""

def foo1():
    """my docstring"""


def foo2():
    """my docstring"""
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


def foo3():
    123  # B018: 4, "Constant"
    a = 2
    "str"
    3  # B018: 4, "Constant"
    (1,)  # bad  # B018: 4, "Tuple"
    (2, 3)  # bad  # B018: 4, "Tuple"
    t = (4, 5)  # good


def foo4():
    a = 1
    b = 2
    c = 3
    d = 4
    result = a * b
    +c * d  # B018: 4, "BinOp"
    a * b  # B018: 4, "BinOp"
    +a * b  # B018: 4, "BinOp"
    -1 * 2  # B018: 4, "BinOp"
    1 * 2 + 3  # B018: 4, "BinOp"
    a + 1  # B018: 4, "BinOp"
    ~a  # B018: 4, "UnaryOp"
    not a  # B018: 4, "UnaryOp"
    a.attr  # B018: 4, "Attribute"
    (x for x in range(10))  # B018: 4, "GeneratorExp"
    return result


def foo5():
    a = [1, 2]
    a.sort()  # good: method call has side effects
    len(a)  # good: function call (could have side effects)
    print(a)  # good: function call
    list(x for x in a)  # good: function call wrapping generator
