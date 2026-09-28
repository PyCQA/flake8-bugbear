# OPTIONS: select=["B913"]

# Python 3.15 allows dict unpacking in dict comprehensions, so
# `ast.DictComp.value` may be None. The finder must not crash on it.

for left, right, _ in zip(xs, ys, limits):  # B913: 17
    consume(left, right, {**d for d in dicts})

for left, right, _ in zip(xs, ys, limits):
    consume(left, right, {**d for d in dicts}, _)
