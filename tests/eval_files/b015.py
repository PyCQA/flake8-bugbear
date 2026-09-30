"""
Unused comparisons are flagged except inside exception/warning assertions.
Expected diagnostics are marked inline.
"""

assert 1 == 1

1 == 1  # B015: 0

assert 1 in (1, 2)

1 in (1, 2)  # B015: 0


if 1 == 2:
    pass


def test():
    assert 1 in (1, 2)

    1 in (1, 2)  # B015: 4


data = [x for x in [1, 2, 3] if x in (1, 2)]


class TestClass:
    1 == 1  # B015: 4


# Comparisons can intentionally raise or warn through overloaded operators.
with pytest.raises(TypeError):
    a == b

with raises(TypeError):
    a != b

with self.assertRaises(TypeError):
    a < b

with self.assertRaisesRegex(TypeError, "unsupported"):
    a in b

with self.assertRaisesRegexp(TypeError, "unsupported"):
    a not in b

with pytest.warns(UserWarning):
    a == b

with self.assertWarns(UserWarning):
    a == b

with self.assertWarnsRegex(UserWarning, "deprecated"):
    a == b

with warns(UserWarning):
    a == b

# Check all context managers and nested control flow.
with unrelated(), pytest.raises(TypeError):
    a == b

with pytest.raises(TypeError):
    if condition:
        a == b

# Defining a function does not execute the comparison inside it.
with pytest.raises(TypeError):

    def nested():
        a == b  # B015: 8


with pytest.raises(TypeError):

    async def nested_async():
        a == b  # B015: 8


# Do not suppress unrelated context managers or comparisons after the block.
with unrelated():
    a == b  # B015: 4

with other.raises(TypeError):
    a == b  # B015: 4

with pytest.fixture():
    a == b  # B015: 4

with raises:
    a == b  # B015: 4

a == b  # B015: 0
