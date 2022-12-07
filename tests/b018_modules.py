"""
Should emit:
B018 - on lines 9-18
"""

a = 2
"str"  # Str (no raise)
f"{int}"  # JoinedStr (no raise)
1j  # Number (complex)
1  # Number (int)
1.0  # Number (float)
b"foo"  # Binary
True  # NameConstant (True)
False  # NameConstant (False)
None  # NameConstant (None)
[1, 2]  # list
{1, 2}  # set
{"foo": "bar"}  # dict
