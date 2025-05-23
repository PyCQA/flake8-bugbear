import unittest
import warnings

import pytest
from pytest import raises, warns

with pytest.raises(TypeError): # B908: 0
    a = 1 + "x"
    b = "x" + 1
print(a, b)


class SomeTestCase(unittest.TestCase):
    def test_func_raises(self):
        with self.assertRaises(TypeError): # B908: 8
            a = 1 + "x"
            b = "x" + 1
        print(a, b)

    def test_func_raises_regex(self):
        with self.assertRaisesRegex(TypeError): # B908: 8
            a = 1 + "x"
            b = "x" + 1
        print(a, b)

    def test_func_raises_regexp(self):
        with self.assertRaisesRegexp(TypeError): # B908: 8
            a = 1 + "x"
            b = "x" + 1
        print(a, b)

    def test_raises_correct(self):
        with self.assertRaises(TypeError):
            print("1" + 1)


with raises(Exception): # B017: 0 # B908: 0
    "1" + 1
    "2" + 2

with pytest.warns(Warning): # B908: 0
    print("print before warning")
    warnings.warn("some warning", stacklevel=1)

with warns(Warning): # B908: 0
    print("print before warning")
    warnings.warn("some warning", stacklevel=1)

# should not raise an error
with pytest.raises(TypeError):
    print("1" + 1)

with pytest.warns(Warning):
    warnings.warn("some warning", stacklevel=1)

with raises(Exception): # B017: 0
    raise Exception("some exception")
