
X = 1
False  # bad  # B018: 0, "Constant"


def func(y):
    a = y + 1
    5.5  # bad  # B018: 4, "Constant"
    return a


class TestClass:
    GOOD = [1, 3]
    [5, 6]  # bad  # B018: 4, "List"

    def method(self, xx, yy=5):
        t = (xx,)
        (yy,)  # bad  # B018: 8, "Tuple"

        while 1:
            i = 3
            4  # bad  # B018: 12, "Constant"
            for n in range(i):
                j = 5
                1.5  # bad  # B018: 16, "Constant"
                if j < n:
                    u = {1, 2}
                    {4, 5}  # bad  # B018: 20, "Set"
                elif j == n:
                    u = {1, 2, 3}
                    {4, 5, 6}  # bad  # B018: 20, "Set"
                else:
                    u = {2, 3}
                    {4, 6}  # bad  # B018: 20, "Set"
                    try:
                        1j  # bad  # B018: 24, "Constant"
                        r = 2j
                    except Exception:
                        r = 3j
                        5  # bad  # B018: 24, "Constant"
                    finally:
                        4j  # bad  # B018: 24, "Constant"
                        r += 1
                    return u + t
