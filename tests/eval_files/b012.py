def a():
    try:
        pass
    finally:
        return  # warning  # B012: 8, ""


def b():
    try:
        pass
    finally:
        if 1 + 0 == 2 - 1:
            return  # warning  # B012: 12, ""


def c():
    try:
        pass
    finally:
        try:
            return  # warning  # B012: 12, ""
        except Exception:
            pass


def d():
    try:
        try:
            pass
        finally:
            return  # warning  # B012: 12, ""
    finally:
        pass


def e():
    if 1 == 2 - 1:
        try:

            def f():
                try:
                    pass
                finally:
                    return  # warning  # B012: 20, ""

        finally:
            pass


def g():
    try:
        pass
    finally:

        def h():
            return  # no warning

        e()


def i():
    while True:
        try:
            pass
        finally:
            break  # warning  # B012: 12, ""

            def j():
                while True:
                    break  # no warning


def h():
    while True:
        try:
            pass
        finally:
            continue  # warning  # B012: 12, ""

            def j():
                while True:
                    continue  # no warning


def k():
    try:
        pass
    finally:
        while True:
            break  # no warning
        while True:
            continue  # no warning
        while True:
            return  # warning  # B012: 12, ""


while True:
    try:
        pass
    finally:
        continue  # warning  # B012: 8, ""

while True:
    try:
        pass
    finally:
        break  # warning  # B012: 8, ""
