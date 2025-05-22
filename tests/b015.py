"""
Should emit:
B015 - on lines 8, 12, 22, 29
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
