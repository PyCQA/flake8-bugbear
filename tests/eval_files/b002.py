def this_is_all_fine(n):
    x = n + 1
    y = 1 + n
    z = +x + y
    return +z


def this_is_buggy(n):
    x = ++n  # B002: 8
    return x


def this_is_buggy_too(n):
    return ++n  # B002: 11
