assert (x for x in a)  # B044: 0
assert [x for x in a]
assert {x for x in a}
assert {x: y for x, y in a}
