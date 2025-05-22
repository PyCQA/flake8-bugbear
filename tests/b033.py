"""
Should emit:
B033 - on lines 6-12, 16, 18
"""

test = {1, 2, 3, 3, 5} # B033: 17, "3"
test = {"a", "b", "c", "c", "e"} # B033: 23, "'c'"
test = {True, False, True} # B033: 21, "True"
test = {None, True, None} # B033: 20, "None"
test = {3, 3.0} # B033: 11, "3.0"
test = {1, True} # B033: 11, "True"
test = {0, False} # B033: 11, "False"
multi_line = {
    "alongvalueeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    1,
    True, # B033: 4, "True"
    0,
    False, # B033: 4, "False"
}

test = {1, 2, 3, 3.5, 5}
test = {"a", "b", "c", "d", "e"}
test = {True, False}
test = {None}
