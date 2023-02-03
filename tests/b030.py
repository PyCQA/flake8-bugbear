try:
    pass
except (ValueError, (RuntimeError, (KeyError, TypeError))):  # ok
    pass

try:
    pass
except 1:  # error
    pass

try:
    pass
except (1, ValueError):  # error
    pass
