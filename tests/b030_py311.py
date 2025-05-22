try:
    pass
except* (ValueError, (RuntimeError, (KeyError, TypeError))):  # error # B030: 0
    pass

try:
    pass
except* (ValueError, *(RuntimeError, *(KeyError, TypeError))):  # ok
    pass

try:
    pass
except* 1:  # error # B030: 0
    pass

try:
    pass
except* (1, ValueError):  # error # B030: 0
    pass

try:
    pass
except* (ValueError, *(RuntimeError, TypeError)):  # ok
    pass


def what_to_catch():
    return (ValueError, TypeError)


try:
    pass
except* what_to_catch():  # ok
    pass


try:
    pass
except* a.b[1].c:  # ok
    pass
