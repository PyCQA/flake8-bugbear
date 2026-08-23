# OPTIONS: select=["B913"]

# Errors: direct underscore targets whose values are unused.
for left, right, _ in zip(xs, ys, limits):  # B913: 17
    consume(left, right)

for [left, right, _] in zip(xs, ys, limits):  # B913: 18
    consume(left, right)

for left, right, _, _ in zip(xs, ys, limits, extras):  # B913: 17
    consume(left, right)

for left, _ in zip(xs, limits):  # B913: 10
    consume(left)

for left, _, right in zip(xs, limits, ys):  # B913: 10
    consume(left, right)

# Stores, nested bindings, and repeated targets do not use every zip value.
for left, right, _ in zip(xs, ys, limits):  # B913: 17
    consume(left, right)
    _ = object()

for left, right, _ in zip(xs, ys, limits):  # B913: 17
    consume(left, right, [item for _ in xs])

for left, right, _, _ in zip(xs, ys, limits, extras):  # B913: 17
    consume(left, right, _)

# No errors: the discarded value is used or its iteration semantics are explicit.
for left, right, _ in zip(xs, ys, limits):
    consume(left, right, _)

for left, right, _ in zip(xs, ys, limits):
    consume(left, right)
else:
    consume(_)

for left, right, _ in zip(xs, ys, limits, strict=True):
    consume(left, right)

# No errors: the target-to-argument mapping is not direct and statically known.
for left, *_rest, _ in zip(xs, ys, limits):
    consume(left)

for left, right, _ in zip(xs, *iterables):
    consume(left, right)

for left, right, (value, _) in zip(xs, ys, pairs):
    consume(left, right, value)

# No errors: nested or mixed repeated underscore targets are conservative skips.
for left, (middle, right), _ in zip(xs, pairs, limits):
    consume(left, middle, right)

for _, left, _ in zip(xs, ys, limits):
    consume(left)

for _, _ in zip(xs, ys):
    pass

for left, right, _ in builtins.zip(xs, ys, limits):
    consume(left, right)

for left, right, _ in zip(xs, ys):
    consume(left, right)

# No errors: these reads refer to the zip target rather than a nested binding.
for left, right, _ in zip(xs, ys, limits):
    consume(left, right, [consume(_) for item in items])

for left, right, _ in zip(xs, ys, limits):
    consume(left, right, [item for item in _])

for left, right, _ in zip(xs, ys, limits):
    consume(left, right, [item for _.value in items])

for left, right, _ in zip(xs, ys, limits):
    consume(left, right, [item for target[_] in items])

for left, right, _ in zip(xs, ys, limits):
    _ += 1
    consume(left, right)
