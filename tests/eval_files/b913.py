class MyError_no_args(Exception):
    def __init__(self):  # safe
        ...


class MyError_args_good(Exception):
    def __init__(self, foo, bar=3):
        super().__init__(foo, bar)


class MyError_args_bad(Exception):
    def __init__(self, foo, bar=3):  # B913: 4
        super().__init__(foo)


class MyError_kwonlyargs(Exception):
    def __init__(self, *, foo):  # B913: 4
        super().__init__(foo=foo)


class MyError_kwargs(Exception):
    def __init__(self, **kwargs):  # B913: 4
        super().__init__(**kwargs)


class MyError_vararg_good(Exception):
    def __init__(self, *args):  # safe
        super().__init__(*args)


class MyError_vararg_bad(Exception):
    def __init__(self, *args):  # B913: 4
        super().__init__()


class MyError_args_nothing(Exception):
    def __init__(self, *args): ...  # B913: 4


class MyError_nested_init(Exception):
    def __init__(self, x):  # B913: 4
        if True:
            super().__init__(x)

class MyError_posonlyargs(Exception):
    def __init__(self, x, /, y):
        super().__init__(x, y)

# triggers if class name ends with, or
# if it inherits from a class whose name ends with, any of
# 'Error', 'Exception', 'ExceptionGroup', 'Warning', 'ExceptionGroup'
class Anything(ValueError):
    def __init__(self, x): ...  # B913: 4
class Anything2(BaseException):
    def __init__(self, x): ...  # B913: 4
class Anything3(ExceptionGroup):
    def __init__(self, x): ...  # B913: 4
class Anything4(UserWarning):
    def __init__(self, x): ...  # B913: 4

class MyError(Anything):
    def __init__(self, x): ...  # B913: 4
class MyException(Anything):
    def __init__(self, x): ...  # B913: 4
class MyExceptionGroup(Anything):
    def __init__(self, x): ...  # B913: 4
class MyWarning(Anything):
    def __init__(self, x): ...  # B913: 4

class ExceptionHandler(Anything):
    def __init__(self, x): ...  # safe

class FooException:
    def __init__(self, x): ...
