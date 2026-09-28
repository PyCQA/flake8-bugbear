"""
Should emit:
B018 - on lines 10-21
"""


def arithmetic(a, b, c, d):
    # meant as the continuation of the line above (#452)
    result = a * b
    +c * d  # B018: 4, "BinOp"
    a + 1  # B018: 4, "BinOp"
    a - b  # B018: 4, "BinOp"
    a / b  # B018: 4, "BinOp"
    a // b  # B018: 4, "BinOp"
    a % b  # B018: 4, "BinOp"
    a**b  # B018: 4, "BinOp"
    -1  # B018: 4, "UnaryOp"
    -a  # B018: 4, "UnaryOp"
    +a  # B018: 4, "UnaryOp"
    ~a  # B018: 4, "UnaryOp"
    not a  # B018: 4, "UnaryOp"
    return result


def overloaded_operators(task1, task2, matrix):
    # shifts, bitwise operators and `@` are overloaded for their side effects,
    # e.g. Airflow's `task1 >> task2`
    task1 >> task2
    task1 << task2
    task1 | task2
    task1 & task2
    task1 ^ task2
    matrix @ matrix
    task1 + (task2 >> task1)


def side_effects(a, f):
    # an operand that calls, yields or assigns is not useless
    f() + 1
    -f()
    (x := a) + 1
    (yield a) + 1


async def awaits(a):
    (await a) + 1


def expected_to_raise(a, raises):
    # directly in a `try` or `with` block, an operation may be run to see it raise
    with raises(TypeError):
        a + "x"
    try:
        -a
    except TypeError:
        pass
