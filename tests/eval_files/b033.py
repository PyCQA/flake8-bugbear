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

# Signed numbers are represented by UnaryOp nodes in the AST.
test = {-1, -1} # B033: 12, "-1"
test = {1, +1} # B033: 11, "1"
test = {+1, 1} # B033: 12, "1"
test = {-1, -1.0} # B033: 12, "-1.0"
test = {0, -0.0} # B033: 11, "-0.0"
test = {1j, +1j} # B033: 12, "1j"
test = {-1j, -1j} # B033: 13, "(-0-1j)"
test = {-1, -True} # B033: 12, "-1"

test = {-1, 1, -2.0, 2.0, -1j, 1j}
value = 1
test = {-value, -value}
test = {1 + 2, 3}
test = {~1, ~1}
test = {-"text", -"text"}
