# OPTIONS: select=["B950"], max_doc_length=50
# Code limit: default 79 (+10%). Doc limit: 50 (+10%).
"""Module docstring, short line.

A docstring line that is far too long for the doc limit, yes it is  # B950: 86, 86, 50
.......................................................
"""

# Code lines use max-line-length only.
x = ["a long-ish line of code, but within the code limit.........."]
y = ["a line of code that is long enough to be too long for the code limit", 12345]  # B950: 105, 105, 79

# A comment-only line that is far too long for the doc limit, yes it is  # B950: 91, 91, 50
# .....................................................
# https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com
# NOT OK: https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com  # B950: 111, 111, 50
z = 1  # a trailing comment makes this line longer than the doc limit, but it is code
z = 1  # a trailing comment that is so long that it exceeds the code limit as a whole  # B950: 107, 107, 79


def f():
    """Function docstring.

    A docstring line that is far too long for the doc limit, yes it is  # B950: 90, 90, 50
    https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com
    ...................................................
    """
    # An indented comment that is far too long for the doc limit, yes it is  # B950: 95, 95, 50
    return (
        1  # trailing comment, long enough to be over the doc limit but not code limit
        # A comment inside parentheses that is far too long for the doc limit  # B950: 97, 97, 50
    )


class C:
    """Class docstring, far too long for the doc limit, yes it is indeed  # B950: 92, 92, 50
    """

    attr = """\
    A string assigned to a name is code, so only the code limit applies to it
    """
    other = """\
    A string assigned to a name that is too long even for the code limit, yes yes  # B950: 103, 103, 79
    """


def g():
    "A one-line docstring that is far too long for the doc limit, yes it is"  # B950: 96, 96, 50


"A bare string statement that is far too long for the doc limit, yes it is"  # B950: 95, 95, 50

b"A bare bytes statement that is far too long for the doc limit, yes it is"  # B018: 0, "Constant" # B950: 119, 119, 50
"A string statement followed by code is code, as for W505"; w = 1
