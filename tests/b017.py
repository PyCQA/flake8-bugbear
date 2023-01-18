"""
Should emit:
B017 - on lines 24, 26, 28, 31 and 32.
"""
import asyncio
import unittest

import pytest

CONSTANT = True


def something_else() -> None:
    for i in (1, 2, 3):
        print(i)


class Foo:
    pass


class Foobar(unittest.TestCase):
    def evil_raises(self) -> None:
        with self.assertRaises(Exception):
            raise Exception("Evil I say!")
        with self.assertRaises(Exception, msg="Generic exception"):
            raise Exception("Evil I say!")
        with pytest.raises(Exception):
            raise Exception("Evil I say!")
        # These are evil as well but we are only testing inside a with statement
        self.assertRaises(Exception, lambda x, y: x / y, 1, y=0)
        pytest.raises(Exception, lambda x, y: x / y, 1, y=0)

    def context_manager_raises(self) -> None:
        with self.assertRaises(Exception) as ex:
            raise Exception("Context manager is good")
        with pytest.raises(Exception) as pyt_ex:
            raise Exception("Context manager is good")

        self.assertEqual("Context manager is good", str(ex.exception))
        self.assertEqual("Context manager is good", str(pyt_ex.value))

    def regex_raises(self) -> None:
        with self.assertRaisesRegex(Exception, "Regex is good"):
            raise Exception("Regex is good")
        with pytest.raises(Exception, match="Regex is good"):
            raise Exception("Regex is good")

    def non_context_manager_raises(self) -> None:
        self.assertRaises(ZeroDivisionError, lambda x, y: x / y, 1, y=0)
        pytest.raises(ZeroDivisionError, lambda x, y: x / y, 1, y=0)

    def raises_with_absolute_reference(self):
        with self.assertRaises(asyncio.CancelledError):
            Foo()
        with pytest.raises(asyncio.CancelledError):
            Foo()
