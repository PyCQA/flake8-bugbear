try:
    pass
except (ValueError, (RuntimeError, (KeyError, TypeError))):  # error
    pass

try:
    pass
except (ValueError, *(RuntimeError, *(KeyError, TypeError))):  # ok
    pass

try:
    pass
except 1:  # error
    pass

try:
    pass
except (1, ValueError):  # error
    pass

try:
    pass
except (ValueError, *(RuntimeError, TypeError)):  # ok
    pass


def what_to_catch():
    return (ValueError, TypeError)


try:
    pass
except what_to_catch():  # ok
    pass


try:
    pass
except a.b[1].c:  # ok
    pass
