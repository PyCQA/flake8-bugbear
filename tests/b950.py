#! Ignore long shebang fooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Assumes the default allowed line length of 79

"line is fine"
"                              line               is           fine          "
"                              line               is        still fine          "
"                              line               is    no longer fine by any measures, yup"
"line is fine again"

# Ensure URL/path on it's own line is fine
"https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com"
"NOT OK: https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com"
# https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com
# NOT OK: https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com
#
#: Okay
# This
#                                                                     almost_empty_line_too_long

# This
#                                                                      almost_empty_line_too_long

# Long empty line
"""
                                                                                                                                                                
"""
