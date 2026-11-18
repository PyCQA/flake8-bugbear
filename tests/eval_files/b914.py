"""
Should emit:
B914 - on lines marked below
"""

# A missing comma in a collection or a call
__all__ = ["alpha", "beta" "gamma"]  # B914: 20
CHOICES = ("red", "green" "blue")  # B914: 18
NAMES = {"one", "two" "three"}  # B914: 16
LOOKUP = {"key": "va" "lue"}  # B914: 17
OTHER = {"ke" "y": 1}  # B914: 9
parser.add_argument("-x" "--extra", help="extra")  # B914: 20
parser.add_argument("-v", help="show " "more")  # B914: 31
Literal["a", "b" "c"]  # B914: 13
print(
    "a" "b"  # B914: 4
)

# The strings may be on a line with other items and with different quotes
values = ["a", 'b' "c", 'd']  # B914: 15
values = [b"a" b"b"]  # B914: 10
values = [r"a" "b", "c"]  # B914: 10
values = ["""a""" """b"""]  # B914: 10
values = [f"{values}" "b"]  # B914: 10
values = [f"{values}" f"{values}"]  # B914: 10
values = [f"{'a' 'b'}", "c"]
values = ["a"]  # one string
values = ["a", "b"]  # two items

# Implicit concatenation spread over lines is a common way to write a long string
values = [
    "a"
    "b",
    "c",
]
values = [
    "a",  # comment
    "b"  # comment
    "c",
]
print(
    "first part "
    "second part"
)

# Only the first of two strings on a line is reported once per run
values = ["a", "b" "c" "d", "e"]  # B914: 15
values = [
    "a",
    "b" "c"  # B914: 4
    "d",
]

# Not in brackets, or the only thing in parentheses
text = "a" "b"
text = ("a" "b")
text = (
    "a" "b"
)
values = ["a", ("b" "c")]
values = [("a" "b"), "c"]
print(("a" "b"))
print(("a" "b"), "c")
print("a", ("b" "c"))
print(not ("a" "b"))

# Anything else in the parentheses makes it a tuple, or an expression
values = ("a" "b",)  # B914: 10
values = ("a" "b" % x)  # B914: 10
values = (x, "a" "b")  # B914: 13
print(("a" "b", "c"))  # B914: 7

# Several of them
values = ["a" "b", "c" "d"]  # B914: 10  # B914: 19

# Brackets inside f-strings are not looked at
values = [f"{x['a' 'b']}", "c"]
values = [f"{ {'a' 'b': 1} }", "c"]

# The report is on the line of the pair, not on the first line of a long run
values = [
    "first part of a long string "
    "second part "
    "x" "y"  # B914: 4
]
values = [
    "a" "b"  # B914: 4
    "c" "d",
]
values = [
    "a"
    "b",
    "c" "d"  # B914: 4
    "e",
]

# `match` and `case` start a statement here, they are not calls
match ("a" "b"):
    case ("a" "b"):
        pass
    case ("a", "b" "c"):  # B914: 15
        pass
