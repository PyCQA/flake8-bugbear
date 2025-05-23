
class A:
    def __init__(self) -> None:
        return 1  # bad # B037: 8

class B:
    def __init__(self, x) -> None:
        if x:
            return  # ok
        else:
            return []  # bad # B037: 12

    class BNested:
        def __init__(self) -> None:
            yield  # bad # B037: 12


class C:
    def func(self):
        pass

    def __init__(self, k="") -> None:
        yield from []  # bad # B037: 8


class D(C):
    def __init__(self, k="") -> None:
        super().__init__(k)
        return None  # bad # B037: 8
    
class E:
    def __init__(self) -> None:
        yield "a" # B037: 8
