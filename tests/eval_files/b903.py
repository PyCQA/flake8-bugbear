class NoWarningsMoreMethods:
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar

    def other_function(self): ...


class NoWarningsClassAttributes:
    spam = "ham"

    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar


class NoWarningsComplicatedAssignment:
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar
        self.spam = " - ".join([foo, bar])


class NoWarningsMoreStatements:
    def __init__(self, foo, bar):
        foo = " - ".join([foo, bar])
        self.foo = foo
        self.bar = bar


class Warnings: # B903: 0
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar


class WarningsWithDocstring: # B903: 0
    """A docstring should not be an impediment to a warning"""

    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar


class WarningsExplicitObjectBase(object): # B903: 0
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar


class NoWarningsExceptionSubclass(ValueError):
    """A namedtuple can't replace a subclass of another class"""

    def __init__(self, foo): # B042: 4
        self.foo = foo


class NoWarningsDictSubclass(dict):
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar


class NoWarningsAttributeBase(module.Base):
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar
