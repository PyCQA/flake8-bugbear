"""
Should emit:
B018 - on lines 9-18
"""

a = 2
"str"  # Str (no raise)
f"{int}"  # JoinedStr (no raise)
1j  # Number (complex)  # B018: 0, "Constant"
1  # Number (int)  # B018: 0, "Constant"
1.0  # Number (float)  # B018: 0, "Constant"
b"foo"  # Binary  # B018: 0, "Constant"
True  # NameConstant (True)  # B018: 0, "Constant"
False  # NameConstant (False)  # B018: 0, "Constant"
None  # NameConstant (None)  # B018: 0, "Constant"
[1, 2]  # list  # B018: 0, "List"
{1, 2}  # set  # B018: 0, "Set"
{"foo": "bar"}  # dict  # B018: 0, "Dict"
(1,)  # bad  # B018: 0, "Tuple"
(2, 3)  # bad  # B018: 0, "Tuple"
t = (4, 5)  # good
