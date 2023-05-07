import unittest

import pytest

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
