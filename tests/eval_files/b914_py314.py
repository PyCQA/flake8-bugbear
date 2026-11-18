"""
Should emit:
B914 - on lines marked below
"""

# t-strings are strings too, but they can't be mixed with other strings
values = [t"a" t"b"]  # B914: 10
values = [t"{values}" t"{values}"]  # B914: 10
values = [t"{values['a' 'b']}", "c"]
values = (t"a" t"b")
values = [t"a", t"b"]
