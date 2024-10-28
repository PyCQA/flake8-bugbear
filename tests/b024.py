import abc
import abc as notabc
from abc import ABC, ABCMeta
from abc import abstractmethod
from abc import abstractmethod as abstract
from abc import abstractmethod as abstractaoeuaoeuaoeu
from abc import abstractmethod as notabstract

import foo

"""
Should emit:
B024 - on lines 17, 52, 58, 69, 74, 123, 129
"""


class Base_1(ABC):  # error
    def method(self):
        foo()


class Base_2(ABC):
    @abstractmethod
    def method(self):
        foo()


class Base_3(ABC):
    @abc.abstractmethod
    def method(self):
        foo()


class Base_4(ABC): # safe
    @notabc.abstractmethod
    def method(self):
        foo()


class Base_5(ABC):
    @abstract
    def method(self):
        foo()


class Base_6(ABC):
    @abstractaoeuaoeuaoeu
    def method(self):
        foo()


class Base_7(ABC):  # error
    @notabstract
    def method(self):
        foo()


class MetaBase_1(metaclass=ABCMeta):  # error
    def method(self):
        foo()


class MetaBase_2(metaclass=ABCMeta):
    @abstractmethod
    def method(self):
        foo()


class abc_Base_1(abc.ABC):  # error
    def method(self):
        foo()


class abc_Base_2(metaclass=abc.ABCMeta):  # error
    def method(self):
        foo()


class notabc_Base_1(notabc.ABC):  # safe
    def method(self):
        foo()


class multi_super_1(notabc.ABC, abc.ABCMeta):  # safe
    def method(self):
        foo()


class multi_super_2(notabc.ABC, metaclass=abc.ABCMeta):  # safe
    def method(self):
        foo()


class non_keyword_abcmeta_1(ABCMeta):  # safe
    def method(cls):
        foo()


class non_keyword_abcmeta_2(abc.ABCMeta):  # safe
    def method(self):
        foo()


# very invalid code, but that's up to mypy et al to check
class keyword_abc_1(metaclass=ABC):  # safe
    def method(self):
        foo()


class keyword_abc_2(metaclass=abc.ABC):  # safe
    def method(self):
        foo()


# safe, see https://github.com/PyCQA/flake8-bugbear/issues/293
class abc_annasign_empty_class_variable_1(ABC):
    foo: int
    def method(self):
        foo()


# *not* safe, see https://github.com/PyCQA/flake8-bugbear/issues/471
class abc_assign_class_variable(ABC):
    foo = 2
    def method(self):
        foo()


class abc_annassign_class_variable(ABC):  # *not* safe, see #471
    foo: int = 2
    def method(self):
        foo()


# this doesn't actually declare a class variable, it's just an expression
# this is now filtered out by not having a method
class abc_set_class_variable_4(ABC):
    foo


class abc_class_no_method_1(ABC):
    pass


class abc_class_no_method_2(ABC):
    foo()
