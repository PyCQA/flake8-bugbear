import unittest
import warnings

import pytest
from pytest import raises, warns

with pytest.raises(TypeError):
    a = 1 + "x"
    b = "x" + 1
print(a, b)


class SomeTestCase(unittest.TestCase):
    def test_func_raises(self):
        with self.assertRaises(TypeError):
            a = 1 + "x"
            b = "x" + 1
        print(a, b)

    def test_func_raises_regex(self):
        with self.assertRaisesRegex(TypeError):
            a = 1 + "x"
            b = "x" + 1
        print(a, b)

    def test_func_raises_regexp(self):
        with self.assertRaisesRegexp(TypeError):
            a = 1 + "x"
            b = "x" + 1
        print(a, b)

    def test_raises_correct(self):
        with self.assertRaises(TypeError):
            print("1" + 1)


with raises(Exception):
    "1" + 1
    "2" + 2

with pytest.warns(Warning):
    print("print before warning")
    warnings.warn("some warning", stacklevel=1)

with warns(Warning):
    print("print before warning")
    warnings.warn("some warning", stacklevel=1)

# should not raise an error
with pytest.raises(TypeError):
    print("1" + 1)

with pytest.warns(Warning):
    warnings.warn("some warning", stacklevel=1)

with raises(Exception):
    raise Exception("some exception")
