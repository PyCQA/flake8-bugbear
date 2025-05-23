def a():
    try:
        pass
    except* Exception:
        pass
    finally:
        return  # warning  # B012: 8, "*"


def b():
    try:
        pass
    except* Exception:
        pass
    finally:
        if 1 + 0 == 2 - 1:
            return  # warning  # B012: 12, "*"


def c():
    try:
        pass
    except* Exception:
        pass
    finally:
        try:
            return  # warning  # B012: 12, "*"
        except* Exception:
            pass
