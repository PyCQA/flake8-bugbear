"""
Should emit:
B033 - on lines 6-12, 16, 18
"""

test = {1, 2, 3, 3, 5}
test = {"a", "b", "c", "c", "e"}
test = {True, False, True}
test = {None, True, None}
test = {3, 3.0}
test = {1, True}
test = {0, False}
multi_line = {
    "alongvalueeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    1,
    True,
    0,
    False,
}

test = {1, 2, 3, 3.5, 5}
test = {"a", "b", "c", "d", "e"}
test = {True, False}
test = {None}
