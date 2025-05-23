"""
Should emit:
B019 - on lines 73, 77, 81, 85, 89, 93, 97, 101
"""

import functools
from functools import cache, cached_property, lru_cache


def some_other_cache(): ...


class Foo:
    def __init__(self, x):
        self.x = x

    def compute_method(self, y): ...

    @some_other_cache
    def user_cached_method(self, y): ...

    @classmethod
    @functools.cache
    def cached_classmethod(cls, y): ...

    @classmethod
    @cache
    def other_cached_classmethod(cls, y): ...

    @classmethod
    @functools.lru_cache
    def lru_cached_classmethod(cls, y): ...

    @classmethod
    @lru_cache
    def other_lru_cached_classmethod(cls, y): ...

    @staticmethod
    @functools.cache
    def cached_staticmethod(y): ...

    @staticmethod
    @cache
    def other_cached_staticmethod(y): ...

    @staticmethod
    @functools.lru_cache
    def lru_cached_staticmethod(y): ...

    @staticmethod
    @lru_cache
    def other_lru_cached_staticmethod(y): ...

    @functools.cached_property
    def some_cached_property(self): ...

    @cached_property
    def some_other_cached_property(self): ...

    # Remaining methods should emit B019
    @functools.cache  # B019: 5
    def cached_method(self, y): ...

    @cache  # B019: 5
    def another_cached_method(self, y): ...

    @functools.cache()  # B019: 5
    def called_cached_method(self, y): ...

    @cache()  # B019: 5
    def another_called_cached_method(self, y): ...

    @functools.lru_cache  # B019: 5
    def lru_cached_method(self, y): ...

    @lru_cache  # B019: 5
    def another_lru_cached_method(self, y): ...

    @functools.lru_cache()  # B019: 5
    def called_lru_cached_method(self, y): ...

    @lru_cache()  # B019: 5
    def another_called_lru_cached_method(self, y): ...