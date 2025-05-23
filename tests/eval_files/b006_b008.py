import collections
import datetime as dt
import logging
import operator
import random
import re
import time
import types
from operator import attrgetter, itemgetter, methodcaller
from types import MappingProxyType


# B006
# Allow immutable literals/calls/comprehensions
def this_is_okay(value=(1, 2, 3)): ...


async def and_this_also(value=tuple()):
    pass


def frozenset_also_okay(value=frozenset()):
    pass


def mappingproxytype_okay(
    value=MappingProxyType({}), value2=types.MappingProxyType({})
):
    pass


def re_compile_ok(value=re.compile("foo")):
    pass


def operators_ok(
    v=operator.attrgetter("foo"),
    v2=operator.itemgetter("foo"),
    v3=operator.methodcaller("foo"),
):
    pass


def operators_ok_unqualified(
    v=attrgetter("foo"),
    v2=itemgetter("foo"),
    v3=methodcaller("foo"),
):
    pass


def kwonlyargs_immutable(*, value=()): ...


# Flag mutable literals/comprehensions


def this_is_wrong(value=[1, 2, 3]): ...  # B006: 24


def this_is_also_wrong(value={}): ...  # B006: 29


def and_this(value=set()): ...  # B006: 19


def this_too(value=collections.OrderedDict()): ...  # B006: 19


async def async_this_too(value=collections.defaultdict()): ...  # B006: 31


def dont_forget_me(value=collections.deque()): ...  # B006: 25


# N.B. we're also flagging the function call in the comprehension
def list_comprehension_also_not_okay(default=[i**2 for i in range(3)]):  # B006: 45  # B008: 60
    pass


def dict_comprehension_also_not_okay(default={i: i**2 for i in range(3)}):  # B006: 45  # B008: 63
    pass


def set_comprehension_also_not_okay(default={i**2 for i in range(3)}):  # B006: 44 # B008: 59
    pass


def kwonlyargs_mutable(*, value=[]): ...  # B006: 32


# Recommended approach for mutable defaults
def do_this_instead(value=None):
    if value is None:
        value = set()


# B008
# Flag function calls as default args (including if they are part of a sub-expression)
def in_fact_all_calls_are_wrong(value=time.time()): ...  # B008: 38


def f(when=dt.datetime.now() + dt.timedelta(days=7)):  # B008: 11 # B008: 31
    pass


def can_even_catch_lambdas(a=(lambda x: x)()): ...  # B008: 29


# Recommended approach for function calls as default args
LOGGER = logging.getLogger(__name__)


def do_this_instead_of_calls_in_defaults(logger=LOGGER):
    # That makes it more obvious that this one value is reused.
    ...


# Handle inf/infinity/nan special case
def float_inf_okay(value=float("inf")):
    pass


def float_infinity_okay(value=float("infinity")):
    pass


def float_plus_infinity_okay(value=float("+infinity")):
    pass


def float_minus_inf_okay(value=float("-inf")):
    pass


def float_nan_okay(value=float("nan")):
    pass


def float_minus_NaN_okay(value=float("-NaN")):
    pass


def float_infinity_literal(value=float("1e999")):
    pass


# But don't allow standard floats
def float_int_is_wrong(value=float(3)):  # B008: 29
    pass


def float_str_not_inf_or_nan_is_wrong(value=float("3.14")):  # B008: 44
    pass


# B006 and B008
# We should handle arbitrary nesting of these B008.
def nested_combo(a=[float(3), dt.datetime.now()]):  # B006: 19 # B008: 20 # B008: 30
    pass


# Don't flag nested B006 since we can't guarantee that
# it isn't made mutable by the outer operation.
def no_nested_b006(a=map(lambda s: s.upper(), ["a", "b", "c"])):  # B008: 21
    pass


# B008-ception.
def nested_b008(a=random.randint(0, dt.datetime.now().year)):  # B008: 18 # B008: 36
    pass


# Ignore lambda contents since they are evaluated at call time.
def foo(f=lambda x: print(x)):
    f(1)
