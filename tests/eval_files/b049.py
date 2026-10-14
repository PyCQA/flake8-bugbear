import abc
import functools
from abc import ABC, abstractmethod


class Wrong(ABC):
    # abstractmethod applied to the result of property/classmethod/staticmethod
    # raises AttributeError ("__isabstractmethod__ ... is not writable").
    @abstractmethod  # B049: 5, "property"
    @property
    def a(self):
        return 1

    @abstractmethod  # B049: 5, "classmethod"
    @classmethod
    def b(cls):
        return 1

    @abstractmethod  # B049: 5, "staticmethod"
    @staticmethod
    def c():
        return 1

    @abc.abstractmethod  # B049: 5, "property"
    @property
    def d(self):
        return 1

    @abstractmethod  # B049: 5, "a.setter"
    @a.setter
    def a(self, value):
        return 1

    @abstractmethod  # B049: 5, "a.getter"
    @a.getter
    def a(self):
        return 1

    @abstractmethod  # B049: 5, "a.deleter"
    @a.deleter
    def a(self):
        return 1

    @abstractmethod  # B049: 5, "classmethod"
    @classmethod
    @property
    def e(cls):
        return 1

    # decorators in between do not matter, the order of the two still does
    @abstractmethod  # B049: 5, "staticmethod"
    @some_decorator
    @staticmethod
    def f():
        return 1

    @abstractmethod  # B049: 5, "property"
    @property
    async def g(self):
        return 1


class WrongAsync(ABC):
    @abstractmethod  # B049: 5, "staticmethod"
    @staticmethod
    async def h():
        return 1


# Correct order: abstractmethod is the innermost decorator.
class Right(ABC):
    @property
    @abstractmethod
    def a(self):
        return 1

    @a.setter
    @abstractmethod
    def a(self, value):
        return 1

    @classmethod
    @abstractmethod
    def b(cls):
        return 1

    @staticmethod
    @abstractmethod
    def c():
        return 1

    @classmethod
    @property
    @abstractmethod
    def d(cls):
        return 1

    @property
    @some_decorator
    @abc.abstractmethod
    def e(self):
        return 1

    # abstractmethod outermost is fine when the inner decorators return
    # functions (or objects that accept attributes).
    @abstractmethod
    @some_decorator
    def f(self):
        return 1

    @abstractmethod
    @functools.lru_cache  # B019: 5
    def g(self):
        return 1

    # functools.cached_property does not propagate __isabstractmethod__, so here
    # abstractmethod has to be the OUTER decorator. Not flagged by B049.
    @abstractmethod
    @functools.cached_property
    def h(self):
        return 1

    @functools.cached_property
    @abstractmethod
    def i(self):
        return 1

    # unrelated decorators / lookalikes
    @abstractmethod
    @my.property
    def j(self):
        return 1

    @abstractmethod
    def k(self):
        return 1

    @property
    def l(self):
        return 1


# the decorators are applied no matter what the enclosing scope is
@abstractmethod  # B049: 1, "property"
@property
def free_function(self):
    return 1


class Qualified(ABC):
    @abstractmethod  # B049: 5, "Base.value.setter"
    @Base.value.setter
    def value(self, v):
        return 1
