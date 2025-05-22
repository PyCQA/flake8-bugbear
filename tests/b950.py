#! Ignore long shebang fooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Assumes the default allowed line length of 79

"line is fine"
"                              line               is           fine          "
"                              line               is        still fine          "
"                              line               is    no longer fine by any measures, yup" # B950: 113, 113, 79
"line is fine again"

# Ensure URL/path on it's own line is fine
"https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com"
"NOT OK: https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com"  # B950: 125, 125, 79
# https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com
# NOT OK: https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com  # B950: 125, 125, 79
#
#: Okay
# This
#                                                                     almost_empty_line_too_long

# This
#                                                                      almost_empty_line_too_long # B950: 118, 118, 79

# Long empty line
"""
                                                                                                                                                                
"""
"https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com  # noqa"
"https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com  # type: ignore"
"https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com  # noqa: F401"
"https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com  # pragma: no cover"
"https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com#noqa:F401, B950"
"https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com  # type: ignore[some-code]"
"https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com # type: ignore[some-code]"
"https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com # type: ignore[some-code] # noqa: F401"
"https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com  # noqa: F401 # type:ignore[some-code]"
"NOT OK: https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com  # noqa" # B950: 132, 132, 79
"NOT OK: https://foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.com  # type: ignore" # B950: 140, 140, 79
