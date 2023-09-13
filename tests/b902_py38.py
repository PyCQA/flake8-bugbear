def not_a_method(arg1, /): ...


class NoWarnings:
    def __init__(self, /):
        def not_a_method_either(arg1, /): ...

    def __new__(cls, /, *args, **kwargs): ...

    def method(self, arg1, /, *, yeah): ...

    async def async_method(self, arg1, /, *, yeah): ...

    @classmethod
    def someclassmethod(cls, arg1, with_default=None, /): ...

    @staticmethod
    def not_a_problem(arg1, /): ...


class Warnings:
    def __init__(i_am_special, /): ...

    def almost_a_class_method(cls, arg1, /): ...

    def almost_a_static_method(): ...

    @classmethod
    def wat(self, i_like_confusing_people, /): ...

    def i_am_strange(*args, **kwargs):
        self = args[0]

    def defaults_anyone(self=None, /): ...

    def invalid_kwargs_only(**kwargs): ...

    def invalid_keyword_only(*, self): ...

    async def async_invalid_keyword_only(*, self): ...


class Meta(type):
    def __init__(cls, name, bases, d, /): ...

    @classmethod
    def __prepare__(metacls, name, bases, /):
        return {}


class OtherMeta(type):
    def __init__(self, name, bases, d, /): ...

    @classmethod
    def __prepare__(cls, name, bases, /):
        return {}

    @classmethod
    def first_arg_mcs_allowed(mcs, value, /): ...


def type_factory():
    return object


class CrazyBases(Warnings, type_factory(), metaclass=type):
    def __init__(self): ...


class RuntimeError("This is not a base"):
    def __init__(self): ...


class ImplicitClassMethods:
    def __new__(cls, /, *args, **kwargs): ...

    def __init_subclass__(cls, /, *args, **kwargs): ...

    def __class_getitem__(cls, key, /): ...
