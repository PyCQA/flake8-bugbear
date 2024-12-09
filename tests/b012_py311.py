def a():
    try:
        pass
    except* Exception:
        pass
    finally:
        return  # warning


def b():
    try:
        pass
    except* Exception:
        pass
    finally:
        if 1 + 0 == 2 - 1:
            return  # warning


def c():
    try:
        pass
    except* Exception:
        pass
    finally:
        try:
            return  # warning
        except* Exception:
            pass
