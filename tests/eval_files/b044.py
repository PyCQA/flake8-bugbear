assert (x for x in a)  # B044: 0, "generator_expression", "`all()`"
assert [x for x in a]
assert {x for x in a}
assert {x: y for x, y in a}

# always-true values, e.g. a message without its condition
assert "x should be positive"  # B044: 0, "non-empty string", "the condition"
assert b"data"  # B044: 0, "non-empty string", "the condition"
assert f"x should be {x}"  # B044: 0, "f-string", "the condition"
assert 1  # B044: 0, "non-zero number", "the condition"
assert 0.5, "message"  # B044: 0, "non-zero number", "the condition"
assert [x, y]  # B044: 0, "non-empty list", "the condition"
assert [*a, x]  # B044: 0, "non-empty list", "the condition"
assert {x}  # B044: 0, "non-empty set", "the condition"
assert {"key": value}  # B044: 0, "non-empty dict", "the condition"
assert {**a, "key": value}  # B044: 0, "non-empty dict", "the condition"
assert lambda: x  # B044: 0, "lambda", "to call it"

# values that can be falsy, or are handled elsewhere
assert x
assert x, "x should be positive"
assert True
assert False  # B011: 0
assert None
assert ...
assert ""
assert b""
assert f"{x}"
assert 0
assert 0.0
assert []
assert [*a]
assert {*a}
assert {}
assert {**a}
assert ()
assert (x, y)  # F631, from pyflakes
