# column and lineno changes since 3.12
# on <3.12 and columns are 0, and lineno is emitted from the first line if multiline
def foo():
    return "hello"


var = var2 = "hello"

# warnings
f"begin '{var}' end" # B907: 9, "var"
f"'{var}' end" # B907: 3, "var"
f"begin '{var}'" # B907: 9, "var"

f'begin "{var}" end' # B907: 9, "var"
f'"{var}" end' # B907: 3, "var"
f'begin "{var}"' # B907: 9, "var"

f'a "{"hello"}" b' # B907: 5, "'hello'"
f'a "{foo()}" b' # B907: 5, "foo()"

# fmt: off
k = (f'"' # Error emitted here on <py312 (all values assigned the same lineno)
     f'{var}' # B907: 7, "var"
     f'"'
     f'"')

k = (f'"' # error emitted on this line on <py312
     f'{var}' # B907: 7, "var"
     '"'
     f'"')
# fmt: on

f'{"hello"}"{var}"'  # warn for var and not hello # B907: 12, "var"
f'"{var}"{"hello"}'  # warn for var and not hello # B907: 3, "var"
f'"{var}" and {"hello"} and "{var2}"'  # warn for var and var2 # B907: 3, "var" # B907: 29, "var2"
f'"{var}" and "{var2}"'  # warn for both # B907: 3, "var" # B907: 15, "var2"
f'"{var}""{var2}"'  # warn for both # B907: 3, "var" # B907: 10, "var2"

# check that pre-quote & variable is reset if no post-quote is found
f'"{var}abc "{var2}"'  # warn on var2 # B907: 13, "var2"

# check formatting on different contained types
f'"{var}"' # B907: 3, "var"
f'"{var.__str__}"' # B907: 3, "var.__str__"
f'"{var.__str__.__repr__}"' # B907: 3, "var.__str__.__repr__"
f'"{3+5}"' # B907: 3, "3 + 5"
f'"{foo()}"' # B907: 3, "foo()"
f'"{None}"' # B907: 3, "None"
f'"{...}"'  # although f'"{...!r}"' == 'Ellipsis' # B907: 3, "..."
f'"{True}"' # B907: 3, "True"

# alignment specifier
f'"{var:<}"' # B907: 3, "var"
f'"{var:>}"' # B907: 3, "var"
f'"{var:^}"' # B907: 3, "var"
f'"{var:5<}"' # B907: 3, "var"

# explicit string specifier
f'"{var:s}"' # B907: 3, "var"

# empty format string
f'"{var:}"' # B907: 3, "var"

# These all currently give warnings, but could be considered false alarms
# multiple quote marks
f'"""{var}"""' # B907: 5, "var"
# str conversion specified
f'"{var!s}"' # B907: 3, "var"
# two variables fighting over the same quote mark
f'"{var}"{var2}"'  # currently gives warning on the first one # B907: 3, "var"


# ***no warnings*** #

# padding inside quotes
f'"{var:5}"'

# quote mark not immediately adjacent
f'" {var} "'
f'"{var} "'
f'" {var}"'

# mixed quote marks
f"'{var}\""

# repr specifier already given
f'"{var!r}"'

# two variables in a row with no quote mark inbetween
f'"{var}{var}"'

# don't crash on non-string constants
f'5{var}"'
f"\"{var}'"

# sign option (only valid for number types)
f'"{var:+}"'

# integer presentation type specified
f'"{var:b}"'
f'"{var:x}"'

# float presentation type
f'"{var:e%}"'

# alignment specifier invalid for strings
f'"{var:=}"'

# other types and combinations are tested in test_b907_format_specifier_permutations

# don't attempt to parse complex format specs
f'"{var:{var}}"'
f'"{var:5{var}}"'

# even if explicit string type (not implemented)
f'"{var:{var}s}"'
